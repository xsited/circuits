import os, pprint, base64, json
import unittest
import tempfile

from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource, request

import restfulsqlite_server

pp = pprint.PrettyPrinter(indent=2)

class FlaskrTestCase(unittest.TestCase):

    username = 'admin'
    password = restfulsqlite_server.users.get('admin')

    def setUp(self):
        self.appf = Flask(__name__)
        #self.appf.testing = True
        self.app = self.appf.test_client()
        api = Api(self.appf)
        cedb = restfulsqlite_server.CEDatabase(':memory:')
        restfulsqlite_server.add_resources(api, cedb)

    def tearDown(self):
        print 'teardown'

    def aopen(self, url, method='GET'):
        return self.app.open(url,
            method=method,
            headers={
                'Authorization': 'Basic ' + base64.b64encode(self.username + \
                ":" + self.password)
            }
        )

    def test_auth(self):
        rv = self.app.get('/')
        assert 404 == rv.status_code
        rv = self.app.get('/circuits')
        assert 401 == rv.status_code
        rv = self.aopen('/circuits')
        assert 200 == rv.status_code
        #pp.pprint(rv.data)

    def test_empty_db(self):
        rv = self.aopen('/circuits')
        assert json.loads(rv.data) == []
        rv = self.aopen('/endpoints')
        assert json.loads(rv.data) == []

if __name__ == '__main__':
    unittest.main()
