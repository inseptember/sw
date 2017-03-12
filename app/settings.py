'''
Created on 2017年3月12日

@author: WF
'''
import platform
uploadFolder = '/opt/apps/others/users/%s/%s/'
if 'Windows'==platform.system():
    uploadFolder = 'D:/Documents/users/%s/%s/'
ALLOWED_EXTENSIONS = set(['xls', 'xlsx', 'csv'])
SECRET_KEY='secret!'
MAIL_SERVER='inseptember@yeah.net'
MAIL_PORT=25
MAIL_DEFAULT_SENDER='inseptember@yeah.net'
# CELERY_BROKER_URL='redis://127.0.0.1:6379/0'
# CELERY_BACKEND='redis://127.0.0.1:6379/0'
SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://stock_data:stock_data@localhost/stock_data'
# SQLALCHEMY_BINDS={
#     'xxx':'mysql+pymysql://xxx:xxx@localhost/xxx'
# }
UPLOAD_FOLDER=uploadFolder
SQLALCHEMY_TRACK_MODIFICATIONS=True
# REDIS_URL = "redis://127.0.0.1:6379/0"
SEND_FILE_MAX_AGE_DEFAULT = 60