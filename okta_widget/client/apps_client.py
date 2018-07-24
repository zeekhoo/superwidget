import requests
import json


class AppsClient(object):
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'SSWS ' + token
        }

    def set_name_id(self, id, login, nameid):
        url = self.base_url + '/api/v1/apps/{0}/users/{1}'.format(id, login)
        creds = {
            "credentials": {
                "userName": nameid
            }
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(creds))
        return_status = response.status_code
        return return_status

    def list_perms(self, group_id='00g5ve5kcWInHjb1f355'):
        url = self.base_url + '/api/v1/apps/0oa5vjnkB7SlJwtRR355/groups/{0}'.format('00g5ve5kcWInHjb1f355')

        print('url={}'.format(url))
        response = requests.get(url, headers=self.headers)
        return response.content

    def list_perm(self, group_id=''):
        url = self.base_url + '/api/v1/apps/0oa5vjnkB7SlJwtRR355/groups/{0}'.format(group_id)

        print('url={}'.format(url))
        response = requests.get(url, headers=self.headers)
        return response.content

    def update_perm(self, group_id='', perms=[]):
        url = self.base_url + '/api/v1/apps/0oa5vjnkB7SlJwtRR355/groups/{0}'.format(group_id)

        print('url={}'.format(url))
        response = requests.put(url, headers=self.headers, data=json.dumps(perms))
        return response.content
