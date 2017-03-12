'''
Created on 2017年3月12日

@author: WF
'''
from sqlalchemy.dialects.postgresql import JSON, ARRAY, DOUBLE_PRECISION
from app.core import db
from app.helpers import JsonSerializer

class Kdata(db.Model, JsonSerializer):
    __tablename__ = 'k_data'
    date = db.Column(db.String, primary_key=True)
    code = db.Column(db.String, primary_key=True)
    open = db.Column(DOUBLE_PRECISION)
    close = db.Column(DOUBLE_PRECISION)
    high = db.Column(DOUBLE_PRECISION)
    low = db.Column(DOUBLE_PRECISION)
    volume = db.Column(DOUBLE_PRECISION)