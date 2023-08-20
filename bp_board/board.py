from flask import Blueprint , request, session, render_template
from flask import redirect, flash, url_for
from datetime import date
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
    menu = {'ho':0,'nb':1,'us':0,'cr':0,'sc':0,'py':0}
    try:
        _ = session['uid']
    except:
            flash('스케줄을 확인하려면 로그인하여야 합니다.')
            return redirect('/user/login')
    
    menu = {'ho':0,'nb':0,'us':0,'cr':0,'sc':1}
    page = request.args.get('p', default=1, type=int)
    field = request.args.get('f', default='title', type=str)
    query = request.args.get('q', default='', type=str)
    total_board_count = bs.get_board_count(field=field,query=query)[0]
    total_pages = (total_board_count - 1) // bs.LIST_PER_PAGE + 1
    start_page = (page - 1) // bs.PAGE_PER_SCREEN * bs.PAGE_PER_SCREEN + 1
    end_page = min(total_pages, start_page + bs.PAGE_PER_SCREEN - 1)
    page_list = [i for i in range(start_page, end_page + 1)]

    session['current_page'] = page
    model = {'field' : field, 'query':query, 
            'today': date.today().isoformat(),
            'total_pages' : total_pages, 'start_page' : start_page,
            'end_page' : end_page
            }
    board_list= bs.get_board_list(field=field, query=query, page=page)
    board_list = [dict(zip(['bid', 'uid', 'title', 'modTime', 'viewCount', 'replyCount', 'uname'], row)) for row in board_list]
    for board in board_list:
        board['modTime'] = board['modTime'].strftime('%Y-%m-%d')

    return render_template('/prototype/board/list.html',menu=menu,model=model,board_list=board_list, page_list=page_list)

@user_bp_board.route('/detail/<bid>/<uid>', methods=['GET','POST'])
def detail(bid,uid):
    menu = {'ho':0,'nb':1,'us':0,'cr':0,'sc':0,'py':0}
    if uid != session['uid']:
        bs.increase_count('viewCount',bid=bid)
    board = bs.get_board(bid=bid)
    board = dict(zip(['bid', 'uid', 'title', 'content', 'modTime', 'viewCount', 'replyCount', 'files','uname'], board))
    # file는 나중에

    reply_list = rs.get_reply_list(bid=bid)
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
        files = '{"list":[]}'
        s_uid = session['uid']
        params = (s_uid, title, content, files)
        bs.insert_board(params=params)
        return redirect(url_for('user_bp_board.list', p=1, f='', q=''))

@user_bp_board.route('/delete/<bid>', methods=['GET'])
def delete(bid):
    menu = {'ho':0,'nb':1,'us':0,'cr':0,'sc':0,'py':0}
    return render_template('/prototype/board/delete.html', menu=menu, bid=bid)

@user_bp_board.route('/deleteConfirm/<bid>', methods=['GET'])
def delete_confirm(bid):
    bs.delete_board(bid)
    cs = session['current_page']
    return redirect(url_for('user_bp_board.list', p=cs, f='', q=''))