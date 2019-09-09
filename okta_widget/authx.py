from django.conf import settings
import json
import base64
import re
from .configs import *


# Some of the auth settings are configurable- lets get our config.
CONFIG = Config()

def is_logged_in(request):
    return 'id_token' in request.session or 'access_token' in request.session


def set_id_token(request, id_token):
    request.session['id_token'] = json.loads(_decode_payload(id_token))
    request.session['id_token_raw'] = id_token
    #Used instead of a custom django template filter.

    if 'profile' not in request.session:
        request.session['profile'] = {}
    request.session['profile'].update(request.session['id_token'])
    # print('id_Token + profile = {}'.format(request.session['profile']))


def get_id_token_json(request):
    return json.dumps(request.session['id_token'])


def get_id_token(request):
    return request.session['id_token_raw']


def get_access_token(request):
    return request.session['access_token_raw']


def set_access_token(request, access_token):
    request.session['access_token'] = json.loads(_decode_payload(access_token))
    request.session['access_token_raw'] = access_token


def get_access_token_json(request):
    return json.dumps(request.session['access_token'])


def get_profile(request):
    # print('returning profile = {}'.format(request.session['profile']))
    return request.session['profile']


def set_profile(request, prof):
    if 'profile' not in request.session:
        request.session['profile'] = {}
    request.session['profile'].update(prof)
    # print('set profile from userinfo = {}'.format(request.session['profile']))


def logout(request):
    for key in list(request.session.keys()):
        if not re.match('^^pages_js_', key) and key not in ('config', 'subdomain'):
            # print('deleting {}'.format(key))
            del request.session[key]


def logout_all(request):
    for key in list(request.session.keys()):
        del request.session[key]

def sensitive_transactions_access(request):
    conf = CONFIG.get_config(request)

    if conf['app_permissions_claim'] in request.session['id_token']:
        list = _formatted_list(request.session['id_token'][conf['app_permissions_claim']])
        print(list)
        return 'sensitivetransactions' in list
    return False

def is_admin(request):
    if can_delegate(request):
        return True

    conf = CONFIG.get_config(request)

    if conf.app_permissions_claim in request.session['id_token']:
        list = _formatted_list(request.session['id_token'][conf.app_permissions_claim])
        return set(['admin', 'companyadmin']) & set(list)

    return False


def can_delegate(request):
    if 'access_token' in request.session:
        return _can_delegate(request.session['access_token'])
    return False


def _can_delegate(token):
    if 'groupadmin' in token['scp']:
        return True
    return False


def api_access_admin(request, bearer_token):
    conf = CONFIG.get_config(request)
    token = parse_bearer_token(bearer_token)
    # if _can_delegate(token):
    #     return True

    if conf.api_permissions_claim in token:
        return 'admin' in _formatted_list(token[conf.api_permissions_claim])

    return False


def api_access_company_admin(request, bearer_token):
    conf = CONFIG.get_config(request)
    token = parse_bearer_token(bearer_token)
    if _can_delegate(token):
        return True

    if conf.api_permissions_claim in token:
        return set(['companyadmin']) & set(_formatted_list(token[conf.api_permissions_claim]))

    return False

def transfer_authorization(request, bearer_token):
    token = parse_bearer_token(bearer_token)
    conf = CONFIG.get_config(request)

    if conf['api_xfer_auth_claim'] in token:
        print(token[conf['api_xfer_auth_claim']])
        return token[conf['api_xfer_auth_claim']]
    else:
        return 0

    return False

def _formatted_list(claims_array):
    if len(claims_array) <= 0:
        return claims_array
    return [x.lower().replace(" ", "_").replace("_", "") for x in claims_array]


def parse_bearer_token(bearer_token):
    return json.loads(_decode_payload(bearer_token))


def _decode_payload(token):
    try:
        parts = token.split('.')
        payload = parts[1]
        payload += '=' * (-len(payload) % 4)  # add == padding to avoid padding errors in python
        decoded = str(base64.b64decode(payload), 'utf-8')
        return decoded
    except Exception as ex:
        return ex
