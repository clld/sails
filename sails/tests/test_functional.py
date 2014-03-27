from path import path

from clld.tests.util import TestWithApp

import sails


class Tests(TestWithApp):
    __cfg__ = path(sails.__file__).dirname().joinpath('..', 'development.ini').abspath()
    __setup_db__ = False

    def test_home(self):
        res = self.app.get('/', status=200)

    def test_maps(self):
        self.app.get_html('/parameters/NP740')
        self.app.get_json('/parameters/NP740.solr.json')
        self.app.get_html('/combinations/AND3_AND4')
        self.app.get_html('/sources/sdricharabela')