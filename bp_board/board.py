from flask import Blueprint , request, session, render_template
from flask import redirect, flash, url_for
from datetime import datetime
import json, hashlib, base64, math
from werkzeug.utils import secure_filename
import db.board_service as bs
import db.reply_service as rs
import os
from PIL import Image
import utils as ut
user_bp_board = Blueprint('user_bp_board',__name__)
upload_dir = "static"

@user_bp_board.route('/list', methods=['GET','POST'])
def list():
    menu = {'ho':0,'nb':1,'us':0,'cr':0,'sc':0,'py':0}      # top nav에서 클릭된 상태 보여주기위해
    try:
        _ = session['uid']                                  # 로그인 되었으면 진행
    except:
            flash('게시판을 확인하려면 로그인하여야 합니다.')
            return redirect('/user/login')
    
    page = request.args.get('p', default=1, type=int)
    field = request.args.get('f', default='title', type=str)
    query = request.args.get('q', default='', type=str)
    total_board_count = bs.get_board_count(field=field,query=query)[0]
    total_pages = (total_board_count - 1) // bs.LIST_PER_PAGE + 1
    start_page = (page - 1) // bs.PAGE_PER_SCREEN * bs.PAGE_PER_SCREEN + 1
    end_page = min(total_pages, start_page + bs.PAGE_PER_SCREEN - 1)
    page_list = [i for i in range(start_page, end_page + 1)]

    session['current_page'] = page                      # session으로 현재 페이지 전달
    # model dict로 전달
    model = {'field' : field, 'query':query, 
            'today': datetime.now().isoformat().replace('T',' ')[:-7],
            'total_pages' : total_pages, 'start_page' : start_page,
            'end_page' : end_page
            }
    board_list= bs.get_board_list(field=field, query=query, page=page)
    # tuple 타입으로 받은 리스트를 dictionary안의 list로 변환 'modTime'수정해야 해서
    # 안하고 넘겨주면 JSP파일에서 사용하기 힘듬
    board_list = [dict(zip(['bid', 'uid', 'title', 'modTime', 'viewCount', 'replyCount', 'uname'], row)) for row in board_list]
    for board in board_list:
        board['modTime'] = board['modTime'].strftime('%Y-%m-%d-%H-%M-%S')

    return render_template('/prototype/board/list.html',menu=menu,model=model,board_list=board_list, page_list=page_list)

@user_bp_board.route('/detail/<bid>/<uid>', methods=['GET','POST'])
def detail(bid,uid):
    menu = {'ho':0,'nb':1,'us':0,'cr':0,'sc':0,'py':0}
    # 조회하는 게시글이 자기가 작성한 것이 아니면
    if uid != session['uid']:
        # 조회수 증가
        bs.increase_count('viewCount',bid=bid)
    board = bs.get_board(bid=bid)
    # board = dict(zip(['bid', 'uid', 'title', 'content', 'modTime', 'viewCount', 'replyCount', 'files','uname'], board))
    board = dict(zip(['bid', 'uid', 'title', 'content', 'modTime', 'viewCount', 'replyCount', 'files','uname'], board))
    # file는 나중에
    # files list 가져와야함

    reply_list = rs.get_reply_list(bid=bid)     # 댓글 리스트 받아옴
    # tuple 타입으로 받은 댓글 리스트를 JSP에서 사용하기 위해 변환
    reply_list = [dict(zip(['rid', 'comment', 'regTime', 'isMine', 'uid', 'bid', 'uname'], row)) for row in reply_list]
    file_list = ['test_a','test_b','test_c']

    return render_template('/prototype/board/detail.html',menu=menu,board=board, reply_list=reply_list, file_list=file_list)

@user_bp_board.route('/write', methods=['GET','POST'])
def write():
    menu = {'ho':0,'nb':1,'us':0,'cr':0,'sc':0,'py':0}
    if request.method == 'GET':
        return render_template('/prototype/board/write.html',menu=menu)
    else:
        title = request.form['title']
        content = request.form['content']
        # files는 나중에
        # files = request.files['files']
        if 'files' not in request.files:
            filenames= ""
            filenames_json = json.dumps(filenames)
        else:
            files = request.files.getlist('files')
            filenames = []
            for file in files:
                if file.filename == '':
                    # filename 없을 경우 수정 해아함
                    print('file이름 없음')
                if file:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(upload_dir,'upload', filename))
                    filenames.append(filename)
            filenames_json = json.dumps(filenames)
        # uid는 현재 세션의 uid
        s_uid = session['uid']
        params = (s_uid, title, content, filenames_json)
        bs.insert_board(params=params)
        # redirect함 board_list에 1 페이지로
        return redirect(url_for('user_bp_board.list', p=1, f='', q=''))
    
# 게시글 삭제하는 기능
@user_bp_board.route('/delete/<bid>', methods=['GET'])
def delete(bid):
    menu = {'ho':0,'nb':1,'us':0,'cr':0,'sc':0,'py':0}
    return render_template('/prototype/board/delete.html', menu=menu, bid=bid)

@user_bp_board.route('/deleteConfirm/<bid>', methods=['GET'])
def delete_confirm(bid):
    bs.delete_board(bid)
    # 현재 페이지 전달
    cs = session['current_page']
    # 삭제한 당시의 페이지로 이동  / 검색후 삭제하는 경우 도 추가 예정
    return redirect(url_for('user_bp_board.list', p=cs, f='', q=''))

# 게시글 수정
@user_bp_board.route('/update/<bid>', methods=['GET','POST'])
def update(bid):
    if request.method == 'GET':
        menu = {'ho':0,'nb':1,'us':0,'cr':0,'sc':0,'py':0}
        board = bs.get_board(bid)
        board = dict(zip(['bid', 'uid', 'title', 'content', 'modTime', 'viewCount', 'replyCount', 'files','uname'], board))
        return render_template('/prototype/board/update.html', menu=menu, board=board)
    else:
        title = request.form['title']
        content = request.form['content']
        files = request.form.getlist('delFile')
        #######################################
        if 'files' not in request.files:
            filenames= secure_filename(files.filename)
            filenames_json = json.dumps(filenames)
        else:
            filenames = []
            for file in files:
                if file.filename == '':
                    # filename 없을 경우 수정 해아함
                    # 기존 사용? 
                    print('file이름 없음')
                if file:
                    # 기존 업로드한 파일 삭제하는 코드 추가해야함
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(upload_dir,'upload', filename))
                    filenames.append(filename)
            filenames_json = json.dumps(filenames)
        ######################################
        
        params = (title,content,filenames_json,bid)
        bs.update_board(params=params)

        # files : []

        # 수정한 게시글 조회 페이지로 이동
        return redirect(f"/board/detail/{bid}/{session['uid']}")