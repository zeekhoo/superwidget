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

