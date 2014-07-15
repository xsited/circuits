# coding: utf-8

import os
from nose.tools import assert_equals
from modules.json_browser import JSONAppBrowser

# Swtich into a testing environment
os.environ['WEBPY_ENV'] = 'test'

# Import app to test
from code import app


class TestApi():

    def setup(self):
        self.b = JSONAppBrowser(app)

    def teardown(self):
        self.b.reset()
