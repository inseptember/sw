'''
Created on 2017年3月12日

@author: WF
'''
from flask_testing import TestCase
from app import factory
import unittest
from app.stock.services import KDataService

class BaseTestCase(TestCase):
    def create_app(self):
        app = factory.create_app(__name__, '')
        app.config['TESTING'] = True
        return app
    def test_someting(self):
        service = KDataService()
        print(len(service.all()))

if __name__ == '__main__':
    unittest.main()