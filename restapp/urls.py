'''
This module defines application url structure
'''

urls = (

    # L2vpn REST api
    r'/api/l2vpn(?:/(?P<l2vpn_id>[0-9]+))?', 'controllers.l2vpn.L2vpn',

    # Website Index
    '/', 'controllers.index.Index',

    # L2vpn Index
    r'/l2vpn(/.*)?', 'controllers.index.L2vpnIndex',

)
