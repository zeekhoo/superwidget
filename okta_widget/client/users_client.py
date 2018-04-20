import requests
import json


class UsersClient(object):
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'SSWS ' + token
        }

    def create_user(self, user, activate="false"):
        url = self.base_url + '/api/v1/users?activate={}'.format(activate)
        response = requests.post(url, headers=self.headers, data=json.dumps(user))

    def list_users(self, limit=25, search=None):
        url = self.base_url + '/api/v1/users?limit={0}'.format(limit)
        if search is not None:
            url += '&search=profile.login sw "{0}"'.format(search)

        print('url={}'.format(url))
        response = requests.get(url, headers=self.headers)
        return response.content
