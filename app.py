from flask import Flask, render_template, request, redirect, session, flash
from weather_util import get_weather
import utils as ut
import os, random, json
from bp_user.user import user_bp
from bp_crawling.crawling import user_bp_c
from bp_python.python_func import user_bp_p
from bp_open_api.open_api import user_bp_o
from bp_board.board import user_bp_board
from bp_reply.reply import user_bp_reply
from bp_file_controller.file_controller import user_bp_file_controller
from bp_schedule.schedule import user_bp_schedule


app = Flask(__name__)

app.secret_key = 'qwert12345'
app.config['SESSION_COOKIE_PATH'] = '/'
# blueprint 
app.register_blueprint(user_bp,url_prefix='/user')
app.register_blueprint(user_bp_c,url_prefix='/crawling')
app.register_blueprint(user_bp_p,url_prefix='/python')
app.register_blueprint(user_bp_o,url_prefix='/api')
app.register_blueprint(user_bp_board,url_prefix='/board')
app.register_blueprint(user_bp_reply,url_prefix='/reply')
app.register_blueprint(user_bp_file_controller,url_prefix='/file')
app.register_blueprint(user_bp_schedule, url_prefix='/schedule')

# for Error Handling ####################
def page_not_found(e):
    return render_template('prototype/error404.html')
def server_error(e):
    return render_template('prototype/error500.html')

app.register_error_handler(404, page_not_found)
app.register_error_handler(500, server_error)
#########################################

# for AJAX  #############################
@app.before_first_request
def before_first_request():
    global quote,quotes
    global addr
    filename = os.path.join(app.static_folder,'data/todayQuote.txt')
    with open(filename,encoding='utf-8') as f:
        quotes = f.readlines()
    quote = random.sample(quotes,1)[0]
    session['quote'] = quote
    addr = '수원시 장안구'
    session['addr'] = addr
    
@app.route('/change_quote')
def change_quote():
    global quote
    quote = random.sample(quotes,1)[0]
    session['quote'] = quote
    return quote

@app.route('/change_addr')
def change_addr():
    global addr
    addr = request.args.get('addr')
    session['addr'] = addr
    return addr

@app.route('/change_weather')
def weather():
    global addr
    addr = request.values['addr']
    lat_,lon_ = ut.get_coord(addr+'청')
    return get_weather(app,lat_,lon_)

@app.route('/change_profile',methods=['POST'])
def change_profile():
    file_image = request.files['image']
    filename = os.path.join(app.static_folder,f'upload/{file_image.filename}')
    file_image.save(filename)
    mtime = ut.change_profile(app,filename)
    return str(mtime)

#########################################

@app.route('/')
def home():
    menu = {'ho':1,'nb':0,'us':0,'cr':0,'sc':0}
    return render_template('prototype/home.html',menu=menu, weather=get_weather(app),quote=quote,addr=addr)

@app.route('/schedule2') # 수정될 부분
def schedule():
    try:
        _ = session['uid']
    except:
            flash('스케줄을 확인하려면 로그인하여야 합니다.')
            return redirect('/user/login')
    menu = {'ho':0,'nb':0,'us':0,'cr':0,'sc':1}
    # schedule 만들어서 적용 예정
    return render_template('prototype/02.schedule.html',menu=menu, weather=get_weather(app),quote=quote,addr=addr)

@app.route('/self_intr') # 삭제될 부분
def self_intr():
    menu = {'ho':0,'nb':0,'us':1,'cr':0,'sc':0,'py':0}
    return render_template('prototype/self_intr.html',menu=menu, weather=get_weather(app),quote=quote,addr=addr)





if __name__ == '__main__':
    app.run(debug=True)     # 디버그 모드