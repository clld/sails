from path import path

from clld.tests.util import TestWithApp
from clld.db.meta import DBSession

import sails


class Tests(TestWithApp):
    __cfg__ = path(sails.__file__).dirname().joinpath('..', 'development.ini').abspath()
    __setup_db__ = False

    def test_home(self):
        res = self.app.get('/', status=200)

    def test_misc(self):
        self.app.get('/parameters/AND2.tab')
        self.app.get_html('/parameters/NP740')
        self.app.get_html('/parameters/NP740?z=5&lat=0.5&lng=0.5')
        self.app.get_html('/parameters/NP740?z=ff&lat=pp&lng=yy')
        self.app.get_json('/parameters/NP740.solr.json')
        self.app.get_json('/parameters/NP740.geojson?domainelement=NP740-1')
        if str(DBSession.get_bind().url).startswith('postgresql'):
            self.app.get_html('/combinations/AND3_AND4?v1=cff4400')
        self.app.get_html('/sources/sdricharabela')
        self.app.get_html('/languages')
        self.app.get_dt('/values?parameter=AND1')
        self.app.get_html('/languages.map.html?sEcho=1&sSearch_2=araw')
        self.app.get_dt('/parameters?sSearch_0=AND&iSortingCols=1&iSortCol_0=0')
        self.app.get_dt('/parameters?sSearch_2=And&iSortingCols=1&iSortCol_0=2')
        self.app.get_html('/contributions')
        self.app.get_dt('/values?language=qux')
        self.app.get_html('/values.map.html?parameter=AND1&sEcho=1')
