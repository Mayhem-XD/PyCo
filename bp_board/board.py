from flask import Blueprint , request, session, render_template
from flask import redirect, flash
from datetime import date
import json, hashlib, base64, math
from werkzeug.utils import secure_filename
import db.board_service as bs
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
    board_list= bs.get_board_list(field=field, query=query, offset=page)
    board_list = [dict(zip(['bid', 'uid', 'title', 'modTime', 'viewCount', 'replyCount', 'uname'], row)) for row in board_list]
    for board in board_list:
        board['modTime'] = board['modTime'].strftime('%Y-%m-%d')

    return render_template('/prototype/board/list.html',menu=menu,model=model,board_list=board_list, page_list=page_list)

@user_bp_board.route('/detail/<bid>/<uid>', methods=['GET','POST'])
def detail(bid,uid):
    menu = {'ho':0,'nb':1,'us':0,'cr':0,'sc':0,'py':0}


    return None 