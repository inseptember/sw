'''
Created on 2017年3月12日

@author: WF
'''
from app.core import Service
from app.stock import models

class KDataService(Service):
    __model__ = models.Kdata
    def preInit(self):
        Service.preInit(self)
    