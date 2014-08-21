import requests
from pprint import pprint

class Circuit:
    __host = ''
    __url = 'http://{host}/{path}'
    __path_list = 'circuit'
    __path_item = 'circuit/{}'

    __auth=('', '')

    @staticmethod
    def set_host(host):
        Circuit.__host = host

    @staticmethod
    def set_auth(auth):
        Circuit.__auth = auth

    @staticmethod
    def get_url(rowid=None):
        if Circuit.__host == '':
            raise NameError('Specify host')

        if rowid == None:
            return Circuit.__url.format(host=Circuit.__host, path=Circuit.__path_list)
        else:
            return Circuit.__url.format(host=Circuit.__host, path=Circuit.__path_item.format(rowid))

    def update_from_json(self, j):
        self.column_names = j.keys()
        self.__dict__.update(j)


    def __init__(self, rowid):
        self.rowid = rowid
        r = requests.get(Circuit.get_url(self.rowid), auth=Circuit.__auth)
        r.raise_for_status()

        self.update_from_json(r.json())


    def delete(self):
        r = requests.delete(Circuit.get_url(self.rowid), auth=Circuit.__auth)
        r.raise_for_status()


    def update(self):
        r = requests.put(Circuit.get_url(self.rowid),
                data={k: self.__dict__[k] for k in self.column_names}, auth=Circuit.__auth)
        if r.status_code == 400:
            print(r.json())
        r.raise_for_status()

        self.update_from_json(r.json())


    @staticmethod
    def list():
        r = requests.get(Circuit.get_url(), auth=Circuit.__auth)
        r.raise_for_status()
        return r.json()

    @staticmethod
    def columns():
        r = requests.get(Circuit.get_url() + '/columns', auth=Circuit.__auth)
        r.raise_for_status()
        return r.json()

    @staticmethod
    def create(params):
        r = requests.post(Circuit.get_url(), data = params, auth=Circuit.__auth)
        r.raise_for_status()
        return Circuit(r.json()['id'])



#if __name__ == '__main__':

