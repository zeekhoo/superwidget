import requests
import json


class AuthClient(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def authn(self, username, password):
        url = self.base_url + '/api/v1/authn'
        payload = {
            'username': username,
            'password': password
        }
        data = json.dumps(payload)
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, data=data, headers=headers)
        return response


class SessionsClient(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def me(self):
        url = self.base_url + '/api/v1/sessions/me'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)

        return response

