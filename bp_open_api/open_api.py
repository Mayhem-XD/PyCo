from flask import Blueprint , request, session, render_template, Flask
from weather_util import get_weather
import utils as ut
import package as pk

user_bp_o = Blueprint('user_bp_o',__name__)
app = Flask(__name__)

@user_bp_o.route('/stn_rt_location',methods=['GET','POST'])
def stn_rt_location():
    menu = {'ho':0,'nb':0,'us':0,'cr':0,'sc':0,'oa':1}
    if request.method == 'GET':
        return render_template('prototype/open_api/stn_rt_location.html',menu=menu,weather=get_weather(app),quote=session['quote'])
        # return render_template('prototype/api/stn_rt_location.html',menu=menu,weather=get_weather(app),quote=session['quote'],addr=session['addr'])
    else:
        place = request.form['place']
        return ut.get_rtstnar_map(place)

@user_bp_o.route('expect_congestion',methods=['GET','POST'])
def expect_congestion():
    menu = {'ho':0,'nb':0,'us':0,'cr':0,'sc':0,'oa':1}
    if request.method == 'GET':
        return render_template('',menu=menu,weather=get_weather(app),quote=session['quote'])
    else:
        # ajax로 구현할 예정
        pass