import requests
from pprint import pprint

from restfulsqlite_client import RestfulSqliteClient


class C2E(RestfulSqliteClient):

    def get_table_name(self):
        return 'circuits_endpoints'



class Circuit(RestfulSqliteClient):

    def get_table_name(self):
        return 'circuits'

    def create(self, params=None):
        rowid = super(Circuit, self).create(params)
        C2E().create({ 'circuit' : rowid })
        return rowid

    def get_c2e_row(self):
        c2e = C2E().list({ 'circuit' : self.rowid })
        if c2e == []:
            raise NameError('cant find relation of circuit id {}'.format(self.rowid))

        if len(c2e) > 1:
            raise NameError('too many relations {} for circuit id {}'.format(
                len(c2e),
                self.rowid))

        return C2E(c2e[0])


    def get_endpoints(self):
        c2e = self.get_c2e_row()
        return (c2e.endpoint_a, c2e.endpoint_b)

    def set_endpoints(self, ep):
        c2e = self.get_c2e_row()
        c2e.endpoint_a = ep[0].rowid if ep[0] != None else None
        c2e.endpoint_b = ep[1].rowid if ep[1] != None else None
        c2e.update()

    def get_measures(self):
        c2e = self.get_c2e_row()
        return (c2e.measure_a, c2e.measure_b)

    def set_measures(self, me):
        c2e = self.get_c2e_row()
        c2e.measure_a = me[0].rowid if me[0] != None else None
        c2e.measure_b = me[1].rowid if me[1] != None else None
        c2e.update()




class Endpoint(RestfulSqliteClient):

    def get_table_name(self):
        return 'endpoints'

    def get_circuits(self):
        c2e_list = C2E().list({'endpoint_a':self.rowid})
        c2e_list.extend(C2E().list({'endpoint_b':self.rowid}))
        # TODO: make/check c2e_list uniqe?
        return c2e_list


class Measure(RestfulSqliteClient):

    def get_table_name(self):
        return 'measures'


def set_host_and_auth(host, auth):
    RestfulSqliteClient.set_host(host)
    RestfulSqliteClient.set_auth(auth)


if __name__ == '__main__':
    set_host_and_auth('localhost:5555', ('admin', 'secret'))

    #http://stackoverflow.com/questions/5597836/how-can-i-embedcreate-an-interactive-python-shell-in-my-python-program
    import readline # optional, will allow Up/Down/History in the console
    import code
    vars = globals().copy()
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()

