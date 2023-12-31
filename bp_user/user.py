from flask import Blueprint , request, session, render_template, Flask
from flask import redirect, flash
from datetime import datetime
import db.user_service as us
import json, hashlib, base64, math
from werkzeug.utils import secure_filename
import os
from weather_util import get_weather
from PIL import Image
import utils as ut
user_bp = Blueprint('user_bp',__name__)
app = Flask(__name__)
upload_dir = "static"


@user_bp.route('/login', methods=['GET','POST'])
def login():
    menu = {'ho':0,'nb':0,'us':1,'cr':0,'sc':0,'py':0}
    if request.method == 'GET':
        return render_template('/prototype/user/login.html',menu=menu)
    else:
        uid = request.form['uid']
        pwd = request.form['pwd']
        # userService login check
        result = us.login(uid,pwd)
        if result == us.WRONG_PASSWORD:
            flash('잘못된 pwd')
            return redirect('/user/login')
        elif result == us.UID_NOT_EXIST:
            flash('id가 존재하지 않습니다.')
            return redirect('/user/register')
        elif result == us.CORRECT_LOGIN:
            # user 정보 가져옴
            user_info = us.get_user(uid)
            flash(f'{user_info[2]}님 환영합니다.')
            # session 값 
            session['uid'] = uid
            session['uname'] = user_info[2]
            session['email'] = user_info[3]
            if user_info[6]:
                session['profile'] = user_info[6]
            session['addr'] = user_info[7]
            session['currentUserPage'] = math.ceil(us.count_users()[0]/10)
            return redirect('/')
        

@user_bp.route('/logout')
def logout():
    session.pop('uid',None)                 # 설정한 세션값을 삭제
    session.pop('uname',None)
    session.pop('email',None)
    session.pop('profile',None)
    session.pop('currentUserPage',None)
    session.pop('title',None)
    session.pop('addr',None)
    session['addr'] = '수원시 장안구'       # default address
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
                # image 가공
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
    user = us.get_user(uid)             # user 객체 불러옴
    menu = {'ho':0,'nb':0,'us':1,'cr':0,'sc':0,'py':0}
    if request.method =='GET':
        return render_template('/prototype/user/update.html',user=user,menu=menu)
    else:
        # hidden으로 받아옴
        old_filename = request.form['filename']
        uid = request.form['uid']
        hashed_pwd = request.form['hashedPwd']
        old_email = request.form['oldEmail']
        #
        profile = request.files['profile']
        pwd = request.form['pwd']
        pwd2 = request.form['pwd2']
        uname = request.form['uname']
        email = request.form['email']
        addr = request.form['addr']

        email_flag = False
        if '@' not in email:        # email 변경되지 않았으면
            email_flag = True
        
        pwd_flag = False
        if pwd != None and len(pwd)>1 and pwd == pwd2:      # pwd 변경 되었으면
            pwd_sha256 = hashlib.sha256(pwd.encode())
            hashed_pwd = base64.b64encode(pwd_sha256.digest()).decode('utf-8')
            pwd_flag = True

        if profile and profile.content_type.startswith('image/'):
                if (old_filename is not None) and len(old_filename)>5:      # profile 업로드 되었으면
                    old_file = os.path.join(upload_dir, 'profile', old_filename)
                    os.remove(old_file)                                     # 기존 파일 삭제함
                img = Image.open(profile)
                filename = secure_filename(profile.filename)
                profile_path = os.path.join(upload_dir, 'profile', filename)
                profile.save(profile_path)
                ut.center_image(img).save(profile_path, format='png')       # 이미지 가공해서
                mtime = os.stat(profile_path).st_mtime
                timestamp = datetime.fromtimestamp(mtime).strftime('%Y%m%d%H%M%S')
                new_fname = f'{timestamp}.png'                              # 현재시간 기반 이름으로 저장
                os.rename(profile_path, os.path.join(upload_dir, 'profile', new_fname))
                filename = new_fname
        else:
            filename = old_filename
        
        if email_flag:                          # email 수정 X 이면 
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

@user_bp.route('/checkUid', methods=['GET'])        # update 화면에서 ajax로 중복여부 체크하기 위해
def check_uid():
    uid = request.args.get('uid')
    return us.check_uid(uid)

@user_bp.route('/list/<int:page>', methods=["GET"])     # 로그인 안되어있으면 user_list 화면에 접근 못함
def user_list(page):
    try:
        _ = session['uid']
    except:
            flash('사용자를 확인하려면 로그인하여야 합니다.')
            return redirect('/user/login')
    menu = {'ho':0,'nb':0,'us':1,'cr':0,'sc':0,'py':0}
    total_user = us.count_users()[0]
    total_pages = math.ceil(total_user/10)
    user_list = us.get_user_list(page)
    
    page_list = [i for i in range(1, total_pages+1)]

    return render_template('/prototype/user/list.html', user_list=user_list, page_list=page_list, currentUserPage=page, menu=menu)


