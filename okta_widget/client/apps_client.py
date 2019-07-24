import requests
import json


class AppsClient(object):
    def __init__(self, base_url, token, client_id):
        self.base_url = base_url
        self.client_id = client_id
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'SSWS ' + token
        }

    def get_login_disco_url(self):
        name = 'LoginDisco_{}'.format(self.client_id)
        url = self.base_url + '/api/v1/apps?q={0}'.format(name)
        try:
            response = requests.get(url, headers=self.headers)
            result = json.loads(response.content)[0]['_links']['appLinks'][0]['href'].split('.com')[1]
        except Exception as e:
            print('get_login_disco_url exception {}'.format(e))
            print('url={}'.format(url))
            result = ''
        return result

    def set_name_id(self, login, nameId):
        url = self.base_url + '/api/v1/apps/{0}/users/{1}'.format(self.client_id, login)
        creds = {
            "credentials": {
                "userName": nameId
            }
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(creds))
        return_status = response.status_code
        return return_status

    def get_app_group_by_id(self, group_id=None):
        if group_id is None:
            return {}

        url = self.base_url + '/api/v1/apps/{0}/groups/{1}'.format(self.client_id, group_id)
        # print('url={}'.format(url))
        response = requests.get(url, headers=self.headers)
        return response.content

    def update_app_group(self, group_id=None, perms=[]):
        url = self.base_url + '/api/v1/apps/{0}/groups/{1}'.format(self.client_id, group_id)

        # print('url={}'.format(url))
        if group_id is None:
            return {}
        else:
            response = requests.put(url, headers=self.headers, data=json.dumps(perms))
        return response.content

    def get_schema(self):
        url = self.base_url + '/api/v1/meta/schemas/apps/{}/default'.format(self.client_id)
        # print('url={}'.format(url))
        response = requests.get(url, headers=self.headers)
        return response.content
