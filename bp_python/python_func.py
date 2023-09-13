from flask import Blueprint , request, session, render_template, Flask
from weather_util import get_weather
import utils as ut
import package as pk

user_bp_p = Blueprint('user_bp_p',__name__)
app = Flask(__name__)

# 삭제하거나 대체될 예정
@user_bp_p.route('/hotplace',methods=['GET','POST'])
def hotplace():
    menu = {'ho':0,'nb':0,'us':0,'cr':0,'sc':0,'py':1}
    if request.method == 'GET':
        return render_template('prototype/python/hotplace.html',menu=menu,weather=get_weather(app),quote=session['quote'],addr=session['addr'])
    else:
        place1 = request.form['place1']
        place2 = request.form['place2']
        place3 = request.form['place3']
        places = [place1, place2, place3]
        ut.hot_places(places, app)
        return None

# park_status
@user_bp_p.route('/park_status',methods=['GET','POST'])
def park_status():
    menu = {'ho':0,'nb':0,'us':0,'cr':0,'sc':0,'py':1}
    if request.method == 'GET':
        return render_template('', menu=menu,weather=get_weather(app),quote=session['quote'],addr=session['addr'])
    else:
        pass
        # ajax 예정

# pop_pd_smt
# 수정 될 듯
@user_bp_p.route('/pop_pd_smt',methods=['GET','POST'])
def pop_pd_smt():
    menu = {'ho':0,'nb':0,'us':0,'cr':0,'sc':0,'py':1}
    if request.method == 'GET':
        return render_template('', menu=menu,weather=get_weather(app),quote=session['quote'],addr=session['addr'])
    else:
        smonth = request.form['smonth']
        emonth = request.form['emonth']
        line = request.form['line']
        target = request.form['target']
        pk.show_heatmap(app=app,target=target,smonth=smonth,emonth=emonth)
        #
        pass
        # ajax 예정
        # 입력 파라메타 : 시작일(년월일) 종료일(년월일) 호선 타겟시간
        # 전달 파라메타 : 이미지

# pop_pd
# 다른 기능으로 대체될 예정
@user_bp_p.route('pop_pd',methods=['GET','POST'])
def pop_pd():
    menu = {'ho':0,'nb':0,'us':0,'cr':0,'sc':0,'oa':1}
    if request.method == 'GET':
        return render_template('',menu=menu,weather=get_weather(app),quote=session['quote'])
    else:
        # ajax로 구현할 예정
        pass
