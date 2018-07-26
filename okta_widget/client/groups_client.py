import requests
import json


class GroupsClient(object):
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'SSWS ' + token
        }

    def create_group(self, group):
        url = self.base_url + '/api/v1/groups'.format()
        response = requests.post(url, headers=self.headers, data=json.dumps(group))

    def update_user(self, user, user_id, deactivate="false"):
        url = self.base_url + '/api/v1/users/{}'.format(user_id)
        response = requests.post(url, headers=self.headers, data=json.dumps(user))
        print(response.content)

    def create_user_scoped(self, user, activate="false", group=""):
        url = self.base_url + '/api/v1/users?activate={}'.format(activate)
        response = requests.post(url, headers=self.headers, data=json.dumps(user))

    def list_groups(self, limit=25, search=None):
        url = self.base_url + '/api/v1/groups?limit={}'.format(limit)

        if search:
            url += '&q={}'.format(search)

        print('url={}'.format(url))
        response = requests.get(url, headers=self.headers)
        return response.content

    def get_group_by_id(self, group_id):
        url = self.base_url + '/api/v1/groups/{0}'.format(group_id)

        print('url={}'.format(url))
        response = requests.get(url, headers=self.headers)
        return response.content

