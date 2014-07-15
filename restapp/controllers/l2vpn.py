# coding: utf-8
import web
from web.form import Validator
from modules.json_controller import JSONController
from modules.json_form import (JSONForm, NotFoundError,
                               BooleanInput, StringInput,
                               IntegerInput, valid_choice,
                               valid_mac, valid_ip)


class L2vpn(JSONController):

    Form = JSONForm(
        StringInput(
            'l2vpnid',
            Validator('Cannot be empty', bool),
            Validator('Must contain between 1 and 255 characters',
                      lambda x: 1 <= len(x) <= 255),
        ),
        IntegerInput(
            'port',
            Validator('Must be positive integer',
                      lambda x: not x or int(x) > 0)
        ),
        IntegerInput(
            'protocol',
            Validator('Choose between valid options: udp(1), tcp(2)',
                      valid_choice(1, 2))
        ),
        IntegerInput(
            'encapsulationtype',
            Validator('Choose between valid options: '
                      'other(1), ieee8021q(2), ieee8021ad(3), '
                      'mpls(4), l2tpv3(5), ieee8021ah(6)',
                      valid_choice(*range(1, 7)))
        ),
        StringInput('encapsulationvalue'),
        StringInput(
            's_mac',
            Validator('Enter valid MAC address', valid_mac)
        ),
        StringInput(
            's_address',
            Validator('Cannot be empty', bool),
            Validator('Enter valid IPv4 or IPv6 address', valid_ip),
        ),
        StringInput(
            'd_mac',
            Validator('Enter valid MAC address', valid_mac)
        ),
        StringInput(
            'd_address',
            Validator('Cannot be empty', bool),
            Validator('Enter valid IPv4 or IPv6 address', valid_ip),
        ),
        BooleanInput('status')
    )

    def list(self):
        '''Select l2vpn from database'''
        return web.ctx.db.select('l2vpn').list()

    def get(self, l2vpn_id):
        '''Select l2vpn by id'''
        l2vpn = web.ctx.db.select('l2vpn', where="id = $l2vpn_id",
                                  vars=locals()).list()
        if l2vpn:
            return l2vpn[0]
        else:
            raise NotFoundError()

    def create(self):
        '''Create new l2vpn'''
        form = self.Form()
        if form.validates():
            l2vpn_id = web.ctx.db.insert('l2vpn', **form.d)
            return self.get(l2vpn_id)

    def update(self, l2vpn_id):
        '''Update l2vpn by id and redirect to its url'''
        form = self.Form()
        if form.validates():
            l2vpn = self.get(l2vpn_id)
            web.ctx.db.update('l2vpn', where='id = $l2vpn_id',
                              vars=locals(), **form.d)
            l2vpn.update(**form.d)
            return l2vpn

    def delete(self, l2vpn_id):
        '''Delete l2vpn by id and return deleted l2vpn'''
        l2vpn = self.get(l2vpn_id)
        web.ctx.db.delete('l2vpn', where='id = $l2vpn_id', vars=locals())
        return l2vpn
