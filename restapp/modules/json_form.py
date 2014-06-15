# coding: utf-8
import re
import web
import json
import ipaddress


class ValidationError(web.HTTPError):
    '''`400 Bad Request` error.'''

    headers = {'Content-Type': 'application/json'}

    def __init__(self, errors, headers=None):
        status = '400 Bad Request'
        message = json.dumps(errors)
        web.HTTPError.__init__(self, status, headers or self.headers,
                               unicode(message))


class NotFoundError(web.HTTPError):
    '''`404 Not Found` error.'''

    headers = {'Content-Type': 'application/json'}

    def __init__(self, note='Not Found', headers=None):
        status = '404 Not Found'
        message = json.dumps([{'note': note}])
        web.HTTPError.__init__(self, status, headers or self.headers,
                               unicode(message))


class InternalServerError(web.HTTPError):
    '''`500 Internal Server Error`.'''

    headers = {'Content-Type': 'application/json'}

    def __init__(self, note='Internal Server Error', headers=None):
        status = '500 Internal Server Error'
        message = json.dumps([{'note': note}])
        web.HTTPError.__init__(self, status, headers or self.headers,
                               unicode(message))


class JSONForm(web.form.Form):
    '''Subclass web.py form to parse json input
       and raise validation errors in json format'''

    def serialize_errors(self):
        '''Serializes form's errors'''
        errors = []
        if self.note:
            errors.append({'note': self.note})
        for i in self.inputs:
            if i.note:
                errors.append({'name': i.name, 'note': i.note})
        return errors

    def validates(self, source=None, _validate=True, **kw):
        if not (source or kw):
            try:
                # Try to parse json request
                source = json.loads(web.data())
            except:
                # Assume empty request
                pass

        if super(JSONForm, self).validates(source, _validate, **kw):
            return True
        else:
            raise ValidationError(self.serialize_errors())


class Input(web.form.Input):
    '''Base input class'''


class BooleanInput(Input):
    '''Processes boolean input'''

    def __init__(self, name, *validators, **attrs):
        self.checked = attrs.pop('checked', False)
        super(BooleanInput, self).__init__(name, *validators, **attrs)

    def set_value(self, value):
        if value in ('0', 'false'):
            self.checked = False
        else:
            self.checked = bool(value)

    def get_value(self):
        return self.checked


class StringInput(Input):
    '''Processes string input'''


class IntegerInput(Input):

    def get_value(self):
        try:
            return int(self.value)
        except:
            return None


def valid_ip(value):
    '''Validates ip address'''
    return not value or ipaddress.ip_address(value)


def valid_choice(*choices):
    '''Validates if integer value is in choices'''
    return lambda value: int(value) in choices


MAC_REGEXP = re.compile(r'^([0-9a-f]{2}[:-]){5}([0-9a-f]{2})$', re.I)


def valid_mac(value):
    '''Validates mac address'''
    return not value or bool(MAC_REGEXP.match(str(value)))
