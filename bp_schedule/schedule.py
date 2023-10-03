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
user_bp_schedule = Blueprint('user_bp_schedule',__name__)
app = Flask(__name__)
upload_dir = "static"

@user_bp_schedule.route('/test', methods=['GET','POST'])
def test():
    try:
        _ = session['uid']
    except:
        flash('스케줄을 확인하려면 로그인하여야 합니다.')
        return redirect('/user/login')
    menu = {'ho':0,'nb':0,'us':0,'cr':0,'sc':1}
    return render_template('/my_schedule/schedule.html',menu=menu, weather=get_weather(app))
@user_bp_schedule.route('/insert', methods=['GET','POST'])
def insert():
    pass
@user_bp_schedule.route('/detail/<sid>', methods=['GET','POST'])
def detail(sid):
    pass
@user_bp_schedule.route('/delete/<sid>', methods=['GET','POST'])
def delete(sid):
    pass
@user_bp_schedule.route('/update', methods=['GET','POST'])
def update():
    pass
@user_bp_schedule.route('/insert_anniv', methods=['GET','POST'])
def insert_anniv():
    pass
