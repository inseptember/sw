'''
Created on 2017年3月12日

@author: WF
'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only
from sqlalchemy import text
import logging, time, json, os
from flask_login.login_manager import LoginManager

class Service(object):
    __model__ = None
    __cache__ = {}

    def _isinstance(self, model, raise_error=True):
        rv = isinstance(model, self.__model__)
        if not rv and raise_error:
            raise ValueError('%s is not of type %s' % (model, self.__model__))
        return rv

    def _preprocess_params(self, kwargs):
        kwargs.pop('csrf_token', None)
        return kwargs

    def save(self, model):
        self._isinstance(model)
        db.session.add(model)
        db.session.commit()
        return model

    def all(self):
        return self.__model__.query.all()

    def get(self, id):
        return self.__model__.query.get(id)

    def get_all(self, *ids):
        return self.__model__.query.filter(self.__model__.id.in_(ids)).all()

    def find(self, **kwargs):
        return self.__model__.query.filter_by(**kwargs)
    
    def search(self, *cols, **kwargs):
        
        return self.__model__.query.options(load_only(*cols)).filter_by(**kwargs)
#         return self.find(**kwargs).options(load_only(*cols))
    
    def first(self, **kwargs):
        return self.find(**kwargs).first()

    def get_or_404(self, id):
        return self.__model__.query.get_or_404(id)

    def new(self, **kwargs):
        return self.__model__(**self._preprocess_params(kwargs))

    def create(self, **kwargs):
        return self.save(self.new(**kwargs))

    def update(self, model, **kwargs):
        self._isinstance(model)
        for k, v in self._preprocess_params(kwargs).items():
            setattr(model, k, v)
        self.save(model)
        return model

    def delete(self, model):
        self._isinstance(model)
        db.session.delete(model)
        db.session.commit()
#     def _execute(self, sql):
#         retProxy = db.engine.execute(sql)
#         return retProxy
    def _execute(self, *args):
        retProxy = db.engine.execute(*args)
        return retProxy
    def paginationSql(self, sql, params=dict(start=0, length=50, total=0, order_bys=[])):
        if 'total' not in params or params['total'] == 0:
            _sql = 'select count(t.*) from (%s) as t' % sql
            params['total'] = self._execute(text(_sql)).fetchone()[0]
        order_by_sql = ''
        if len(params['order_bys']) >0:
            for order_by in params['order_bys']:
                if '.' in order_by[0]:
                    order_by[0] = order_by[0].replace('.', "->'") + "'"
            order_by_sql = ' order by ' + ', '.join([x[0] + ' ' + x[1] for x in params['order_bys']])
        _sql = sql + order_by_sql
        if params['length']>0:
            _sql += ' limit %d offset %d' % (params['length'], params['start'] * params['length'])
        q = self.__model__.query.from_statement(text(_sql))
#         q = q.limit(params['length']).offset(params['start'] * params['length'])
        return q, params
        
    def pagination(self, q = None, limit = 50, offset=0):
        if q is None:
            q = self._model_.query
        q = q.limit(limit).offset(offset)
        return q
    
    def query(self, sql=''):
        return self.__model__.query.from_statement(text(sql))
    @property
    def _session(self):
        return db.session
    @property
    def cache(self):
        return self.__cache__
    def getCacheData(self, key, subId, default = None):
        dumpStr = self.cache.hget(key, subId)
        if dumpStr is None:
            return default
        return json.loads(dumpStr)
    def setCacheData(self, key, subId, data):
        self.cache.hset(key,subId, json.dumps(data))
        self.cache.expire(key, 2 * 3600)
    def preInit(self):
        pass

def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)
    return l

logger_user = setup_logger('logger_user', os.path.dirname(os.path.abspath(__file__)) + os.path.sep + 'user_%s.log' % time.strftime('%Y-%m'), logging.INFO)

db = SQLAlchemy()
loginManager = LoginManager()
# mail = Mail()
# mgr = socketio.KombuManager(REDIS_URL)
# sio = socketio.Server(client_manager=mgr, async_mode='threading')
# redis_store = FlaskRedis()

