import requests


class UnidemoClient():
    def __init__(self, url):
        self.url = url

    def get_public_config(self, subdomain):
        url = '{0}/unidemo/public/config/{1}'.format(self.url, subdomain)
        response = requests.get(url)
        return response.content


