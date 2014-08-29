import sqlite3, itertools
import pprint

from flask import Flask
from flask.ext.restful import reqparse, abort, Api, Resource, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
api = Api(app)

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

tname = 'circuits'

arg_p = reqparse.RequestParser()


con = sqlite3.connect('restful.db', check_same_thread=False)
con.row_factory = sqlite3.Row
c = con.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [tname])
if c.fetchone() == None:
    c.execute("""CREATE TABLE {0}
            (service_type text, start_ip_address text, end_ip_address text,
            classifier text, active text, self text, uri text, mgmt_ip text,
            ext_ip text, tuuid text, tunnel_if text, status text)
            """.format(tname))
    con.commit()


c.execute("PRAGMA table_info({})".format(tname))
columns = c.fetchall()
for column in columns:
    type = {
            'text' : str,
            'int' : int,
            'integer' : int
            }[ column['type'] ]
    arg_p.add_argument(column['name'], type=type)


def get_row(rowid):
    c.execute("select * from {} where rowid=?".format(tname), [rowid])
    row = c.fetchone()
    if row == None:
        abort(404, message="row id {} not found".format(rowid))
    else:
        return row


def row2dict(row):
    ret = {}
    for col in columns:
        c_name = str(col['name'])
        r_name = row[c_name]
        ret[c_name] = r_name

    return ret


def get_values_and_names(args):
    val_names = []
    values = []
    for col in columns:
        c_name = col['name']
        c_type = col['type']
        if args[c_name] != None:
            print "got '{}' with '{}'".format(c_name, args[c_name])
            val_names.append(c_name)
            values.append(args[c_name])

    return val_names, values


class Circuit(Resource):
    @auth.login_required
    def get(self, rowid):
        row = get_row(rowid)
        print(row.keys())
        return row2dict(row)


    @auth.login_required
    def delete(self, rowid):
        get_row(rowid)

        c.execute("delete from {} where rowid=?".format(tname), [rowid])
        con.commit()
        return '', 204

    @auth.login_required
    def put(self, rowid):
        get_row(rowid)
        args = arg_p.parse_args()

        val_names, values = get_values_and_names(args)

        update_names = [name + " = ?" for name in val_names]
        print(values)

        ins = "update {0} set {1} where rowid=?".format(
                tname, ', '.join(update_names)
                )
        print(ins)
        values.append(rowid)
        print(values)
        c.execute(ins, values)
        con.commit()

        row = get_row(rowid)
        return row2dict(row)


class RColumns(Resource):
    @auth.login_required
    def get(self):
        return [k['name'] for k in columns]


class RList(Resource):
    @auth.login_required
    def get(self):
        c.execute("select rowid from {}".format(tname))
        clist = list(itertools.chain.from_iterable(c.fetchall()))
        #if clist == []:
        #    abort(404, message="Table '{}' is empty".format(tname))
        return clist


    @auth.login_required
    def post(self):
        args = arg_p.parse_args()
        val_names, values = get_values_and_names(args)

        ins = "insert into {0} ({1}) values ({2})".format(
                tname, ','.join(val_names), ', '.join('?'*len(values))
                )
        print(ins)
        c.execute(ins, values)
        con.commit()

        return { "id" : c.lastrowid }, 201



api.add_resource(RList, '/circuit')
api.add_resource(Circuit, '/circuit/<int:rowid>')
api.add_resource(RColumns, '/circuit/columns')

if __name__ == '__main__':
        app.run('0.0.0.0', 5555, debug=True)

