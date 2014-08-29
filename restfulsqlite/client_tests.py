import os, pprint, time, signal
import unittest

from multiprocessing import Process

from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource, request

import restfulsqlite_server
from circuits_lib import Circuit, Endpoint, Measure, set_host_and_auth

pp = pprint.PrettyPrinter(indent=2)

# sqlite's ":memory:" wont work as desired
testdbname = 'testing.db'

cedb = restfulsqlite_server.CEDatabase(testdbname)


class TestInit(unittest.TestCase):

    username = 'admin'
    password = restfulsqlite_server.users.get('admin')
    host = '127.0.0.1:55577'

    def setUp(self):
        set_host_and_auth(self.host, (self.username, self.password))

    def tearDown(self):
        print "teardown"



class EmpyDbTest(TestInit):
    def test_empty_circuits(self):
        self.assertEqual(Circuit().list(), [])

    def test_empty_endpoints(self):
        self.assertEqual(Endpoint().list(), [])

    def test_empty_measures(self):
        self.assertEqual(Measure().list(), [])


class InsertTest(TestInit):
    def test_circuit_insert(self):
        self.assertEqual(Circuit().create(), 1)
        cedb.c.execute("select * from circuits")
        self.assertEqual(len(cedb.c.fetchall()), 1)
        cedb.c.execute("select * from circuits_endpoints")
        self.assertEqual(len(cedb.c.fetchall()), 1)

    def test_endpoint_insert(self):
        self.assertEqual(Endpoint().create(), 1)
        cedb.c.execute("select * from endpoints")
        self.assertEqual(len(cedb.c.fetchall()), 1)

        self.assertEqual(Endpoint().create(), 2)
        cedb.c.execute("select * from endpoints")
        self.assertEqual(len(cedb.c.fetchall()), 2)

    def test_measurement_insert(self):
        self.assertEqual(Measure().create(), 1)
        cedb.c.execute("select * from measures")
        self.assertEqual(len(cedb.c.fetchall()), 1)


class CETest(TestInit):
    def test_CE_link(self):
        c1 = Circuit(1)
        self.assertEqual(c1.get_endpoints(), (None, None))
        c1.set_endpoints((Endpoint(1), Endpoint(2)))
        self.assertEqual(c1.get_endpoints(), (1, 2))
        cedb.c.execute("select * from circuits_endpoints")
        fall = cedb.c.fetchall()
        self.assertEqual(len(fall), 1)
        self.assertEqual(fall[0]['endpoint_a'], 1)
        self.assertEqual(fall[0]['endpoint_b'], 2)


"""
this is not a "true" unit-tests, because they need some prerequisities,
like web server running and execution in certain order
"""

def run_test(cls):
    suite = unittest.TestLoader().loadTestsFromTestCase(cls)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    restfulsqlite_server.add_resources(api, cedb)
    p = Process(target=app.run, args=('127.0.0.1', 55577))
    p.daemon = True
    p.start()
    time.sleep(1)

    """
    since we have only one server, we need to perform tests in right order
    """
    run_test(EmpyDbTest)
    run_test(InsertTest)
    run_test(CETest)

    p.terminate()
    p.join()

    try:
        os.remove(testdbname)
    except OSError:
        pass

