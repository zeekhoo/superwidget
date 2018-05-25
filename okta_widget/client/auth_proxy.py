import requests
import json


class AuthClient(object):
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def authn(self, username, password):
        url = self.base_url + '/api/v1/authn'
        payload = {
            'username': username,
            'password': password
        }
        data = json.dumps(payload)
        response = requests.post(url, data=data, headers=self.headers)
        return response

    def recovery(self, recoveryToken):
        url = self.base_url + '/api/v1/authn/recovery/token'
        payload = {
            'recoveryToken': recoveryToken
        }
        data = json.dumps(payload)
        response = requests.post(url, data=data, headers=self.headers)
        return response


class SessionsClient(object):
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def me(self):
        url = self.base_url + '/api/v1/sessions/me'
        response = requests.get(url, headers=self.headers)
        return response

