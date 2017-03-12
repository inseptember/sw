'''
Created on 2017年3月12日

@author: WF
'''
import json
from flask import Blueprint
from . import route, getPage
from flask.globals import request
from flask.templating import render_template
from flask_login import (login_user, logout_user , current_user)
from app.core import logger_user

bp = Blueprint('stock', __name__, url_prefix='/stock')

@route(bp, '/')
def lists():
    return json.dumps([])