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
upload_dir = "static"


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
            user_info = us.get_user(uid)
            flash(f'{user_info[2]}님 환영합니다.')
            session['uid'] = uid
            session['uname'] = user_info[2]
            session['email'] = user_info[3]
            session['addr'] = user_info[7]
            return redirect('/')
        

@user_bp.route('/logout')
def logout():
    session.pop('uid',None)                 # 설정한 세션값을 삭제
    session.pop('uname',None)
    session.pop('email',None)
    session.pop('addr',None)
    session['addr'] = '수원시 장안구'
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
        
@user_bp.route('/update/<uid>', methods=['GET','POST'])
def update(uid):
    user = us.get_user(uid)
    menu = {'ho':0,'nb':0,'us':1,'cr':0,'sc':0,'py':0}
    if request.method =='GET':
        return render_template('/prototype/user/update.html',user=user,menu=menu)
    else:
        old_filename = request.form['filename']
        profile = request.files['profile']
        uid = request.form['uid']
        hashed_pwd = request.form['hashedPwd']
        pwd = request.form['pwd']
        pwd2 = request.form['pwd2']
        uname = request.form['uname']
        email = request.form['email']
        addr = request.form['addr']
        old_email = request.form['oldEmail']

        email_flag = False
        if '@' not in email:
            email_flag = True
        
        pwd_flag = False
        if pwd != None and len(pwd)>1 and pwd == pwd2:
            pwd_sha256 = hashlib.sha256(pwd.encode())
            hashed_pwd = base64.b64encode(pwd_sha256.digest()).decode('utf-8')
            pwd_flag = True

        if profile and profile.content_type.startswith('image/'):
                if old_filename:
                    old_file = os.path.join(upload_dir, 'profile', old_filename)
                    os.remove(old_file)
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
        else:
            filename = old_filename
        
        if email_flag:
            email = old_email
        params = (uname,hashed_pwd,email,filename,addr,uid)
        us.update_user(params)
        user = us.get_user(uid)
        session['uid'] = user[0]
        session['uname'] = user[2]
        session['email'] = user[3]
        session['profile'] = user[6]
        session['addr'] = user[7]
        
        if pwd_flag:
            flash('비밀번호가 변경 되었습니다.')
            return redirect('/user/list')
        else:
            return redirect('/user/list')

@user_bp.route('/list', methods=["GET"])
def user_list():
    try:
        _ = session['uid']
    except:
            flash('사용자를 확인하려면 로그인하여야 합니다.')
            return redirect('/user/login')
    menu = {'ho':0,'nb':0,'us':1,'cr':0,'sc':0,'py':0}
    page = int((us.count_users()[0])/10 + 1)
    user_list = us.get_user_list(page)
    return render_template('/prototype/user/list.html',user_list=user_list ,menu=menu)
        
@user_bp.route('/checkUid', methods=['GET'])
def check_uid():
    uid = request.args.get('uid')
    return us.check_uid(uid)


