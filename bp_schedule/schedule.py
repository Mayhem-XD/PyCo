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
    pass
@user_bp_schedule.route('/insert', methods=['GET','POST'])
def insert():
    pass
@user_bp_schedule.route('/detail/<sid>', methods=['GET','POST'])
def detail(sid):
    pass

