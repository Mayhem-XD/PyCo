from flask import Blueprint , request, session, render_template, Flask
from weather_util import get_weather
import utils as ut

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




