from template import render


class Index:

    def GET(self):
        return render.index()


class L2vpnIndex:

    def GET(self, path=''):
        return render.l2vpn()
