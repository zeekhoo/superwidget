import requests
import json
import base64
from django.conf import settings


class OAuth2Client(object):
    def __init__(self, base_url, client_id=None, client_secret=None):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.basic = None
        if client_id is not None and client_secret is not None:
            enc = client_id + ':' + client_secret
            basic = base64.b64encode(enc.encode('ascii'))
            self.basic = str(basic, 'utf-8')

    def token(self, code, redirect_uri, server_id=None):
        if server_id:
            server_id += '/'
        else:
            server_id = ''
        url = self.base_url + '/oauth2/{}v1/token'.format(server_id)
        payload = {
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
            'code': code
        }
        auth = {}
        if self.basic:
            auth = {'Authorization': 'Basic ' + self.basic}
        response = requests.post(url, data=payload, headers=auth)
        tokens = response.json()
        print('tokens = {}'.format(tokens))
        return tokens

    def profile(self, token):
        AUTH_SERVER_ID = settings.AUTH_SERVER_ID
        OKTA_ORG = settings.OKTA_ORG
        iss = 'https://{0}/oauth2/{1}'.format(OKTA_ORG, AUTH_SERVER_ID)

        #iss = _tokenIssuer(token)
        if iss:
            url = iss + '/v1/userinfo'
        else:
            url = self.base_url + '/oauth2/v1/userinfo'
        print('userinfo url={}'.format(url))

        headers = {
            'Authorization': 'Bearer ' + token
        }
        try:
            response = requests.post(url, headers=headers)
            print('response = {}'.format(response))
            profile = response.json()
            return profile
        except Exception as e:
            print('exception: {}'.format(e))


def _tokenIssuer(token):
    iss = None
    try:
        parts = token.split('.')
        payload = parts[1]
        payload += '=' * (-len(payload) % 4)
        decoded = base64.b64decode(payload)
        print('payload = {}'.format(decoded))
        iss = json.loads(decoded)['iss']
    except Exception as e:
        print('there was an exception: {}'.format(e))
        return None
    print('iss = {}'.format(iss))
    return iss


