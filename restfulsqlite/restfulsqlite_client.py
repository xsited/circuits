import requests
from pprint import pprint

class RestfulSqliteClient(object):
    __host = ''
    __auth=('', '')
    __url = 'http://{host}/{path}'


    def get_list_path(self):
        return self.get_table_name()

    def get_item_path(self):
        return self.get_table_name() + '/{}'

    def get_columns_path(self):
        return self.get_table_name() + '/columns'

    @staticmethod
    def set_host(host):
        RestfulSqliteClient.__host = host

    def get_auth(self):
        return RestfulSqliteClient.__auth

    @staticmethod
    def set_auth(auth):
        RestfulSqliteClient.__auth = auth

    @staticmethod
    def format_url(path):
        if RestfulSqliteClient.__host == '':
            raise NameError('Specify host')

        return RestfulSqliteClient.__url.format(
                host=RestfulSqliteClient.__host,
                path=path)

    def list_url(self):
        return self.format_url(self.get_list_path())

    def item_url(self, rowid):
        return self.format_url(self.get_item_path().format(rowid))

    def columns_url(self):
        return self.format_url(self.get_columns_path())

    def list(self, params=None):
        r = requests.get(self.list_url(), data=params, auth=self.get_auth())
        r.raise_for_status()
        return r.json()

    def columns(self):
        r = requests.get(self.columns_url(), auth=self.get_auth())
        r.raise_for_status()
        return r.json()

    def create(self, params=None):
        r = requests.post(self.list_url(), data = params, auth=self.get_auth())
        r.raise_for_status()
        return r.json()['id']


    def update_from_json(self, j):
        self.column_names = j.keys()
        self.__dict__.update(j)


    def __init__(self, rowid=None):
        if rowid != None:
            self.rowid = rowid
            r = requests.get(self.item_url(self.rowid), auth=self.get_auth())
            r.raise_for_status()

            self.update_from_json(r.json())


    def delete(self):
        if self.rowid == None:
            raise NameError('delete called on uninitialized Circuit')

        r = requests.delete(self.item_url(self.rowid), auth=self.get_auth())
        r.raise_for_status()
        self.rowid = None


    def update(self):
        if self.rowid == None:
            raise NameError('update called on uninitialized Circuit')

        r = requests.put(self.item_url(self.rowid),
                data={ k: self.__dict__[k] for k in self.column_names },
                auth=self.get_auth())
        if r.status_code == 400:
            print(r.json())
        r.raise_for_status()

        self.update_from_json(r.json())


