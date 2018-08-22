import json
import requests
import base64

def is_logged_in(request):
    return 'id_token' in request.session or 'access_token' in request.session

def set_id_token(request, id_token):
    request.session['id_token'] = json.loads(_decode_payload(id_token))
    #Used instead of a custom django template filter.

    if 'profile' not in request.session:
        request.session['profile'] = {}
    request.session['profile'].update(request.session['id_token'])
    print('id_Token + profile = {}'.format(request.session['profile']))

def get_id_token_string(request):
    return json.dumps(request.session['id_token'])

def set_access_token(request, access_token):
    request.session['access_token'] = json.loads(_decode_payload(access_token))
    request.session['access_token_raw'] = access_token

def get_access_token_string(request):
    return json.dumps(request.session['access_token'])

# def client_has_scope(access_token, scope):
#     result = False
#     try:
#         if request.session['access_token'] is not None:
#             access_token = json.dumps(request.session['access_token'])
#             result = scope in access_token['scp']
#     except Exception as e:
#         print('exception: {}'.format(e))
#         result = False
#     return result
#
# def get_access_claims(request):
#     try:
#         if request.session['access_token'] is not None:
#             return access_token['claims']
#     except Exception as e:
#         print('exception: {}'.format(e))
#         return None
#     return None

def get_profile(request):
    print('returning profile = {}'.format(request.session['profile']))
    return request.session['profile']


def set_profile(request, prof):
    if 'profile' not in request.session:
        request.session['profile'] = {}
    request.session['profile'].update(prof)
    print('set profile from userinfo = {}'.format(request.session['profile']))


def logout(request):
    for key in list(request.session.keys()):
        print('deleting {}'.format(key))
        del request.session[key]

def is_admin(request):
    return ('admin' in request.session['id_token']['app_permissions'] or
        'company_admin' in request.session['id_token']['app_permissions'])

def api_access_admin(bearer_token):
    token = _parse_bearer_token(bearer_token)
    print('Parsed bearer token = {}'.format(token))
    return 'admin' in token['api_permissions']

def api_access_company_admin(bearer_token):
    token = _parse_bearer_token(bearer_token)
    print('Parsed bearer token = {}'.format(token))
    return 'company_admin' in token['api_permissions']

def _parse_bearer_token(bearer_token):
    return json.loads(_decode_payload(bearer_token))

def _decode_payload(token):
    parts = token.split('.')
    payload = parts[1]
    payload += '=' * (-len(payload) % 4)  # add == padding to avoid padding errors in python
    decoded = str(base64.b64decode(payload), 'utf-8')
    return decoded
