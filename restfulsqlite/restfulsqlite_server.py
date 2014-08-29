import sqlite3, itertools
import pprint

from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource, request
from flask_httpauth import HTTPBasicAuth

from memoize import memoize

auth = HTTPBasicAuth()

users = {
    "admin": "secret"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

pp = pprint.PrettyPrinter(indent=2)

#@app.before_request
def log_request():
    print 'vvvvvvvvvvvvvvv'
    pp.pprint( request.__dict__ )
    print '^^^^^^^^^^^^^^^'


'''
--- endpoint: enabled, external-ip, mgmt-ip, mac-address, state
--- circuits-endpoints: circuit, endpoint_a, endpoint_b, measure_a, measure_b
--- circuits: uuid, tunnel_if, service_type, classifier, active, self, uri, status, start_ip_address, end_ip_address
--- measures: p_tx, p_rx, b_tx, b_rx, throughput, packet_loss, jitter, hops, iperf_latency, netperf_latency
'''

class CEDatabase(object):
    c_name = 'circuits'
    e_name = 'endpoints'
    ce_name = 'circuits_endpoints'
    m_name = 'measures'

    def table_exists(self, table):
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [self.c_name])
        return not self.c.fetchone() == None

    def __init__(self, db_name):
        self.db_name = db_name
        self.con = sqlite3.connect(self.db_name, check_same_thread=False)
        self.con.row_factory = sqlite3.Row
        self.c = self.con.cursor()

        if not self.table_exists(self.c_name):
            self.c.execute("""CREATE TABLE {0}
                    (service_type text, start_ip_address text, end_ip_address text,
                    classifier text, active text, self text, uri text,
                    uuid text, tunnel_if text, status text)
                    """.format(self.c_name))
            self.c.execute("""CREATE TABLE {0}
                    (enabled text, external_ip text, mgmt_ip text, mac_address text, state text)
                    """.format(self.e_name))
            self.c.execute("""CREATE TABLE {0}
                    (circuit int, endpoint_a int, endpoint_b int, measure_a int, measure_b int)
                    """.format(self.ce_name))
            self.c.execute("""CREATE TABLE {0}
                    (p_tx int, p_rx int, b_tx int, b_rx int, throughput int, packet_loss int,
                    jitter int, hops int, iperf_latency int, netperf_latencyi int)
                    """.format(self.m_name))
            self.con.commit()


    #@memoize
    def list_columns(self, table):
        self.c.execute("PRAGMA table_info({})".format(table))
        return self.c.fetchall()

    def get_row(self, rowid, table):
        self.c.execute("select * from {} where rowid=?".format(table), [rowid])
        row = self.c.fetchone()
        if row == None:
            abort(404, message="row id {} int table {} was not found".format(rowid, table))
        else:
            return row

    #@memoize
    def args_for_table(self, tname):
        args_p = reqparse.RequestParser()
        for column in self.list_columns(tname):
            args_p.add_argument(column['name'], type=self.ctype2atype(column['type']))
        return args_p

    def ctype2atype(self ,ctype):
        return {
                'text' : str,
                'int' : int,
                'integer' : int
                }[ ctype ]



def filter_empty_args(args):
    return { k: v for k, v in args.items() if v != None }

class TItem(Resource):
    @auth.login_required
    def get(self, tname, rowid):
        row = self.db.get_row(rowid, tname)
        print(row.keys())
        return dict(row)


    @auth.login_required
    def delete(self, tname, rowid):
        self.db.get_row(rowid, tname)

        self.db.c.execute("delete from {} where rowid=?".format(tname), [rowid])
        self.db.con.commit()
        return '', 204

    @auth.login_required
    def put(self, tname, rowid):
        self.db.get_row(rowid, tname)
        args = self.db.args_for_table(tname).parse_args()

        values = args.values()

        update_names = [name + " = ?" for name in args.keys()]
        print(values)

        ins = "update {0} set {1} where rowid=?".format(
                tname, ', '.join(update_names)
                )
        print(ins)
        values.append(rowid)
        print(values)
        self.db.c.execute(ins, values)
        self.db.con.commit()

        row = self.db.get_row(rowid, tname)
        return dict(row)


class TColumns(Resource):
    @auth.login_required
    def get(self, tname):
        return [ k['name'] for k in list_columns(tname) ]


class TList(Resource):
    @auth.login_required
    def get(self, tname):
        args = self.db.args_for_table(tname).parse_args()
        set_args = filter_empty_args(args)
        if set_args == {}:
            self.db.c.execute("select rowid from {}".format(tname))
        else:
            where = [name + " = ?" for name in set_args.keys()]
            self.db.c.execute("select rowid from {} where {}".format(
                            tname, " AND ".join(where)
                        ), set_args.values())
        clist = [ v[0] for v in self.db.c.fetchall() ]
        return clist


    @auth.login_required
    def post(self, tname):
        args = self.db.args_for_table(tname).parse_args()
        values = args.values()
        pp.pprint(values)

        ins = "insert into {0} ({1}) values ({2})".format(
                tname, ', '.join(args.keys()), ', '.join('?'*len(values))
                )
        print(ins)
        self.db.c.execute(ins, values)
        self.db.con.commit()

        return { "id" : self.db.c.lastrowid }, 201

def add_resources(api, cedb):
    TList.db = cedb
    TColumns.db = cedb
    TItem.db = cedb
    api.add_resource(TList, '/<string:tname>')
    api.add_resource(TColumns, '/<string:tname>/columns')
    api.add_resource(TItem, '/<string:tname>/<int:rowid>')


if __name__ == '__main__':
    app = Flask(__name__)
    cedb = CEDatabase('restful.db')
    api = Api(app)

    add_resources(api, cedb)

    app.run('0.0.0.0', 5555, debug=True)

