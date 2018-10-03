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

    def create_user(self, user, activate=False):
        url = self.base_url + '/api/v1/users?activate={}'.format(activate)
        print('url = {}'.format(url))
        response = requests.post(url, headers=self.headers, data=json.dumps(user))
        print(response.content)
        return response

    def set_password(self, user_id, user):
        url = self.base_url + '/api/v1/users/{}'.format(user_id)
        response = requests.put(url, headers=self.headers, data=json.dumps(user))
        return response

    def activate(self, user_id, send_email=False):
        url = self.base_url + '/api/v1/users/{0}/lifecycle/activate?sendEmail={1}'.format(user_id, send_email)
        response = requests.post(url, headers=self.headers)
        return response

        user_id = response.json().get('id')
        url = self.base_url + '/api/v1/users/{}lifecycle/activate?sendEmail=true'.format(user_id)
        return requests.post(url, headers=self.headers, data=json.dumps(user))

    def update_user(self, user, user_id, deactivate=False):
        url = self.base_url + '/api/v1/users/{}'.format(user_id)
        return requests.post(url, headers=self.headers, data=json.dumps(user))

    # def create_user_scoped(self, user, activate="false", group=""):
    #     url = self.base_url + '/api/v1/users?activate={}'.format(activate)
    #     response = requests.post(url, headers=self.headers, data=json.dumps(user))
    #     user_id = response.json().get('id')
    #
    #     url = self.base_url + '/api/v1/users/{}/lifecycle/activate?sendEmail=true'.format(user_id)
    #     return requests.post(url, headers=self.headers, data=json.dumps(user))

    def set_password(self, user_id, user):
        url = self.base_url + '/api/v1/users/{}'.format(user_id)
        response = requests.post(url, headers=self.headers, data=json.dumps(user))
        return response.content

    def list_users(self, limit=25, search=None):
        url = self.base_url + '/api/v1/users?limit={0}'.format(limit)
        if search is not None:
            url += '&search=profile.login sw "{0}"'.format(search)

        print('url={}'.format(url))
        response = requests.get(url, headers=self.headers)
        return response.content

    def list_user(self, user_id):
        if not user_id or user_id == '':
            return None

        url = self.base_url + '/api/v1/users/{0}'.format(user_id)
        print('url={}'.format(url))
        response = requests.get(url, headers=self.headers)
        return response.content

    def list_users_scoped(self, limit=25, company=None, search=None):
        url = self.base_url + '/api/v1/users?limit={0}'.format(limit)
        s = ''
        if company is not None:
            s = 'profile.companyName eq "{0}"'.format(company)
        if search is not None:
            if s != '':
                s += ' and '
            s += 'profile.login sw "{0}"'.format(search)

        if s != '':
            url += '&search={}'.format(s)

        print('url={}'.format(url))

        response = requests.get(url, headers=self.headers)
        return response.content

    def get_user(self, user_id):
        url = self.base_url + '/api/v1/users/{}'.format(user_id)
        response = requests.get(url, headers=self.headers)
        return response.content

    def get_user_groups(self, user_id):
        url = self.base_url + '/api/v1/users/{}/groups'.format(user_id)
        response = requests.get(url, headers=self.headers)
        return response.content

    def list_factors(self, user_id):
        url = self.base_url + '/api/v1/users/{}/factors'.format(user_id)
        response = requests.get(url, headers=self.headers)
        return response.content

    def enroll_email_factor(self, user_id, email=None):
        url = self.base_url + '/api/v1/users/{}/factors?activate=true'.format(user_id)
        data = {
            'factorType': 'email',
            'provider': 'OKTA',
            "profile": {
                "email": email
            }
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        return response

    # def send_email_challenge(self, user_id, factor_id):
    #     url = self.base_url + '/api/v1/users/{0}/factors/{1}/verify'.format(user_id, factor_id)
    #     response = requests.post(url, headers=self.headers)
    #     return response

    def verify_email_factor(self, user_id, factor_id, pass_code=None):
        url = self.base_url + '/api/v1/users/{0}/factors/{1}/verify'.format(user_id, factor_id)
        data = None
        if pass_code:
            payload = {
                'passCode': pass_code
            }
            data = json.dumps(payload)
        response = requests.post(url, headers=self.headers, data=data)
        return response

