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
        iss = 'https://{0}/oauth2/{1}'.format(settings.OKTA_ORG, settings.AUTH_SERVER_ID)
        #iss = _tokenIssuer(token)
        if iss:
            url = iss + '/v1/userinfo'
        else:
            url = self.base_url + '/oauth2/v1/userinfo'
        print('userinfo url={}'.format(url))

        headers = {'Authorization': 'Bearer ' + token}
        profile = {}
        try:
            response = requests.post(url, headers=headers)
            print('response = {}'.format(response))
            if response.status_code == 200:
                profile = response.json()
        except Exception as e:
            print('exception: {}'.format(e))

        # IMPERSONATION Hack: Get the profile from the "Other" issuer
        if profile == {} and settings.IMPERSONATION_ORG and settings.IMPERSONATION_ORG != 'None'\
                and settings.IMPERSONATION_ORG_AUTH_SERVER_ID and settings.IMPERSONATION_ORG_AUTH_SERVER_ID != 'None':
            url = 'https://{0}/oauth2/{1}/v1/userinfo'.format(settings.IMPERSONATION_ORG, settings.IMPERSONATION_ORG_AUTH_SERVER_ID)
            print('userinfo url={}'.format(url))
            try:
                response = requests.post(url, headers=headers)
                profile = response.json()
            except Exception as e2:
                print('exception2: {}'.format(e2))

        return profile


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


