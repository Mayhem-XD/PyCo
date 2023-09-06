from flask import Blueprint , request, session, render_template, send_file
from flask import redirect, flash, url_for
from datetime import datetime
import json, hashlib, base64, math
from werkzeug.utils import secure_filename
import db.board_service as bs
import db.reply_service as rs
import os
from PIL import Image
import utils as ut
user_bp_file_controller = Blueprint('user_bp_file_controller',__name__)
upload_dir = "static"

# download
@user_bp_file_controller.route('/download/<file>', methods=['GET','POST'])
def download_file(file):
    # upload 한 파일 download
    path = upload_dir + "upload/" + file
    try:
        return send_file(path, as_attachment=True)
    except Exception as e:
        print(e)
        return None
# upload

#profile
@user_bp_file_controller.route('download/<file>', methods=['GET'])
def profile_download(file):
    path = upload_dir + "profile/" + file
    try:
        return send_file(path, as_attachment=True)
    except Exception as e:
        print(e)
        return None