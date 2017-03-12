'''
Created on 2017年3月12日

@author: WF
'''
import eventlet
# from gevent.wsgi import WSGIServer
eventlet.monkey_patch()
from app.api import create_app
if __name__ == '__main__':
    app = create_app()
    app.run('localhost', 8990, threaded=False, debug=True)