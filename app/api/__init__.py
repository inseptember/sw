from functools import wraps

import flask, re, os
from datetime import date
from flask.templating import render_template
from flask.helpers import send_from_directory
from flask.globals import request
from flask_login import (login_user,login_required, logout_user , current_user)

import app.factory as factory
from app.helpers import JSONEncoder
from app.core import loginManager
from flask_login import UserMixin
from app.services import baseService
from app import settings as settings

class User(UserMixin):
    def __init__(self, id, active=True):
        self.id = id
        self.active = active
    def get_id(self):
        return self.id.lower()
    
    @property
    def is_active(self):
        return self.active


def create_app():
    """Use current package to create Flask app from factory.py.
    Define the default login rount and encode method which is JSONEncoder
    Define the default 404 page.
    """
    app = factory.create_app(__name__, __path__)
    app.login_manager.login_view = 'indx.login'
    app.json_encoder = JSONEncoder
    app.errorhandler(404)(page_not_found)
    baseService.load(app)
    return app

def route(bp, *args, **kwargs):
    """Route annotation which need login check.
    This annotation used in each module's route file to define the route path. 
    """
    def decorator(f):
        @bp.route(*args, **kwargs)
        @login_required
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f
    return decorator

def route_non(bp, *args, **kwargs):
    """Route annotation which not need login check
    """
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f
    return decorator

def upload_folder():
    folder = settings.UPLOAD_FOLDER % (current_user.get_id(), str(date.today().month))
    if os.path.exists(folder)==False:
        os.makedirs(folder, 0o775)
    return folder

def page_not_found(e):
    return render_template('404.html'), 404

def getPage(req):
    start = int(req.get('start', 0))
    length = int(req.get('length', 50))
    total = int(req.get('total', 0))
    order_bys = req.get('order_bys','')
    order_bys = [x.split('|') for x in ([] if order_bys=='' else order_bys.split(','))]
    
    return {'start' : start, 'length':length, 'total':total, 'order_bys':order_bys}