'''
Created on 2017年3月12日

@author: WF
'''
import flask, re
from flask.templating import render_template
from flask.helpers import send_from_directory
from flask.globals import request
from flask_login import (login_user, logout_user , current_user)

from app.core import loginManager
from app.api import route, route_non, User


bp = flask.Blueprint('indx', __name__)
@loginManager.user_loader
def load_user(user_id):
    """Check user whether he or she is login, if not return None. 
    and then page will turn to default route
    """
    if user_id and re.match(r'^[a-zA-Z]+\d+$', user_id):
        return User(user_id)
    return None

@route_non(bp, '/login', methods=['GET'])
def login():
    """Login page.
    """
    return render_template('login.html', next=request.args.get('next'))

@route_non(bp, '/login', methods=['POST'])
def loginSubmit():
    """Login Post requst, user just provide an Id and then turn to last page he requets.
    """
    print (request.form['userId'])
    user = User(request.form['userId'])
    login_user(user)
    flask.flash('Logged in successfully.')
    nextpage = request.form['next']
    nextpage = nextpage if nextpage!='' else flask.url_for('.indexpage')
    return flask.redirect(nextpage)

@route(bp, "/logout")
def logout():
    logout_user()
    return flask.redirect(flask.url_for('.indexpage'))

@route_non(bp, '/statics/<path:path>')
def sendStatic(path):
    """This route is used to control the static file."""
    res = send_from_directory('statics', path)
    res.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    res.headers['Cache-Control'] = 'public, max-age=60'
    return res

@route(bp, '/_views/<path:path>')
def sendHtmlPage(path):
    return send_from_directory('templates', path)

@route(bp, '/')
def indexpage():
    return render_template('index.html', userId=current_user.get_id())