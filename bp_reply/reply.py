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
user_bp_reply = Blueprint('user_bp_reply',__name__)
upload_dir = "static"

@user_bp_reply.route('/write',methods=['POST'])
def write():
    bid = request.form['bid']
    board_uid = request.form['uid']
    sess_uid = session['uid']
    comment = request.form['comment']
    isMine = 1 if sess_uid == board_uid else 0
    # comment isMine uid bid
    params = (comment, isMine, sess_uid, bid)
    rs.insert_reply(params=params)
    bs.increase_count('replyCount',bid=bid)
    return redirect(f"/board/detail/{bid}/{session['uid']}")