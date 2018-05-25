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

    def set_password(self, user_id, user):
        url = self.base_url + '/api/v1/users/{}'.format(user_id)
        response = requests.post(url, headers=self.headers, data=json.dumps(user))
        return response.content

    def list_users_scoped(self, limit=25, department="", search=None):
        url = self.base_url + '/api/v1/users?limit={0}'.format(limit)
        url += '&search=status eq "ACTIVE" and profile.department eq "{0}"'.format(department)
        if search is not None:
            url += ' and profile.login sw "{0}"'.format(search)

        print('url={}'.format(url))
        response = requests.get(url, headers=self.headers)
        return response.content
