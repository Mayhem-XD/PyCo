from flask import Blueprint , request, session, render_template
from flask import redirect, flash
from datetime import datetime
import json, hashlib, base64, math
from werkzeug.utils import secure_filename
import os
from PIL import Image
import utils as ut
user_bp_board = Blueprint('user_bp_board',__name__)
upload_dir = "static"

@user_bp_board.route('/list', methods=['GET','POST'])
def login():
    return None