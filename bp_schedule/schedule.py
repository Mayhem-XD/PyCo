from flask import Blueprint , request, session, render_template, Flask
from flask import redirect, flash, url_for, jsonify
from datetime import datetime
import db.user_service as us
import json, hashlib, base64, math
from werkzeug.utils import secure_filename
import os
from weather_util import get_weather
from PIL import Image
import utils as ut
import db.schedule_service as sched
import db.anni_service as anniv
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
    return render_template('/prototype/my_schedule/schedule.html',menu=menu, weather=get_weather(app))

@user_bp_schedule.route('/detail/<sid>', methods=['GET'])
def detail(sid):
    schedule_list = sched.get_schedule(sid)
    schedule_list = [dict(zip(['sid', 'title', 'place', 'startTime', 'endTime', 'isImportant', 'memo'], sch)) for sch in schedule_list]
    
    return jsonify(schedule_list)

@user_bp_schedule.route('/delete/<sid>', methods=['GET'])
def delete(sid):
    return render_template('/prototype/my_schedule/delete.html',sid=sid)

@user_bp_schedule.route('/delete_confirm/<sid>', methods=['GET'])
def delete_confirm(sid):
    sched.delete(sid)
    return redirect(url_for('user_bp_schedule.list'))

@user_bp_schedule.route('/insert', methods=['POST'])
def insert():
    is_important = 0 if request.form['is_important'] == None else 1
    sid = request.form['sid']
    title = request.form['title']
    start_date = request.form['start_date']
    start_time = request.form['start_time']
    end_date = request.form['end_date']
    end_time = request.form['end_time']
    place = request.form['place']
    memo = request.form['memo']
    s_date = start_date.replace('-','')
    start_date_time = f"{start_date}T{start_time}:00"
    end_date_time = f"{end_date}T{end_time}:00"
    uid = session['uid']
    params = (sid, uid, s_date, title, place, start_date_time, end_date_time, memo, is_important)
    sched.insert(params)
    return redirect(url_for('user_bp_schedule.list'))
    



@user_bp_schedule.route('/update', methods=['GET','POST'])
def update():
    menu = {'ho':0,'nb':0,'us':0,'cr':0,'sc':1}
    if request.method == 'GET':
        return render_template('/prototype/my_schedule/update.html',menu=menu, weather=get_weather(app))
    else:
        is_important =   0 if request.form['important']==None else 1 
        sid = request.form['sid']
        title = request.form['title']
        start_date = request.form['start_date']
        start_time = request.form['start_time']
        end_date = request.form['end_date']
        end_time = request.form['end_time']
        place = request.form['place']
        memo = request.form['memo']
        s_date = start_date.replace('-','')
        start_date_time = f"{start_date}T{start_time}:00"
        end_date_time = f"{end_date}T{end_time}:00"
        uid = session['uid']
        params = ( title, s_date, start_date_time, end_date_time, place, memo, is_important, sid, uid)
        sched.update(params)
        return redirect(url_for('user_bp_schedule.calendar'))

@user_bp_schedule.route('/insert_anniv', methods=['POST'])
def insert_anniv():
    aname = request.form['aname']
    is_holiday = 0 if request.form['is_holiday'] == None else 1
    adate = request.form['adate'].replace("-",'')
    params = (aname, is_holiday, adate)
    anniv.insert(params)
    return redirect(url_for('user_bp_schedule.calendar'))
