from flask import Blueprint , request, session, render_template
from flask import redirect, flash
from datetime import datetime
import db.user_service as us
import json, hashlib, base64
from werkzeug.utils import secure_filename
import os
from PIL import Image
import utils as ut
user_bp = Blueprint('user_bp',__name__)
upload_dir = "d:/Temp/"


@user_bp.route('/login', methods=['GET','POST'])
def login():
    menu = {'ho':0,'nb':0,'us':1,'cr':0,'sc':0,'py':0}
    if request.method == 'GET':
        return render_template('/prototype/user/login.html',menu=menu)
    else:
        uid = request.form['uid']
        pwd = request.form['pwd']
        
        result = us.login(uid,pwd)
        if result == us.WRONG_PASSWORD:
            flash('잘못된 pwd')
            return redirect('/user/login')
        elif result == us.UID_NOT_EXIST:
            flash('id가 존재하지 않습니다.')
            return redirect('/user/register')
        elif result == us.CORRECT_LOGIN:
            flash('good')
            session['uid'] = uid
            return redirect('/')
        

@user_bp.route('/logout')
def logout():
    session.pop('uid',None)                 # 설정한 세션값을 삭제
    return redirect('/')

@user_bp.route('/register', methods=['GET','POST'])
def register():
    menu = {'ho':0,'nb':0,'us':1,'cr':0,'sc':0,'py':0}
    if request.method == 'GET':
        return render_template('/prototype/user/register.html',menu=menu)
    else:
        profile = request.files['profile']
        uid = request.form['uid']
        pwd = request.form['pwd']
        pwd2 = request.form['pwd2']
        uname = request.form['uname']
        email = request.form['email']
        addr = request.form['addr']
        # uid check
        user = us.get_user(uid=uid)
        if user != None:
            flash('중복된 ID')
            return redirect('/user/register')
        # pwd check
        if (pwd == pwd2) and (len(pwd)>1):
            pwd_sha256 = hashlib.sha256(pwd.encode())
            hashed_pwd = base64.b64encode(pwd_sha256.digest()).decode('utf-8')
            filename = None
            if profile and profile.content_type.startswith('image/'):
                img = Image.open(profile)
                filename = secure_filename(profile.filename)
                profile_path = os.path.join(upload_dir, 'profile', filename)
                profile.save(profile_path)
                ut.center_image(img).save(profile_path, format='png')
                mtime = os.stat(profile_path).st_mtime
                timestamp = datetime.fromtimestamp(mtime).strftime('%Y%m%d%H%M%S')
                new_fname = f'{timestamp}.png'
                os.rename(profile_path, os.path.join(upload_dir, 'profile', new_fname))
                filename = new_fname
            params = (uid,hashed_pwd,uname,email,filename,addr)
            

            us.register_user(params=params)
            flash('회원가입 완료')
            return redirect('/user/login')
        else:
            flash('잘못된 password')
            return redirect('/user/register')


