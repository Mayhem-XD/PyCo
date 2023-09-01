from flask import Blueprint , request, session, render_template
from flask import redirect, flash, url_for
from datetime import datetime
import json, hashlib, base64, math
from werkzeug.utils import secure_filename
import db.board_service as bs
import db.reply_service as rs
import os
from PIL import Image
import utils as ut
user_bp_file_controller = Blueprint('user_bp_file_controller',__name__)
upload_dir = "static"