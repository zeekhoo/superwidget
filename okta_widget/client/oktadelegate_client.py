import requests
import json


class OktadelegateClient(object):
    def __init__(self, resource_uri, access_token, ssws):
        self.resource_uri = resource_uri
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {0}.{1}'.format(ssws, access_token)
        }

    def delegate_init(self, login):
        url = self.resource_uri + '/delegate/init'
        body = {
            "delegation_target": login
        }
        return requests.post(url, headers=self.headers, data=json.dumps(body))
