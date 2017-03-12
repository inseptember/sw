'''
Created on 2017年3月12日

@author: WF
'''

import os
from flask import Flask
# from flask_socketio import SocketIO
from app import helpers
from celery import Celery
from app.core import db, loginManager

def create_app(package_name, package_path):
    app = Flask(package_name, instance_relative_config=True)
    app.config.from_object('app.settings')    
    db.init_app(app)
    db.app = app
    loginManager.init_app(app)
    helpers.register_blueprints(app, package_name, package_path)
#     celery.init_app(app)
    return app

def make_celery(app=None):
    app = app or create_app('app', os.path.dirname(__file__))
    clr = Celery(app.import_name, backend=app.config['CELERY_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
    clr.conf.update(app.config)
    TaskBase = clr.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, * args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    clr.Task = ContextTask
    return clr