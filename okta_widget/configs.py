from django.contrib.staticfiles.templatetags.staticfiles import static
from .authx import *
from .client.apps_client import AppsClient
import re
import requests
import json
from io import StringIO
from dotenv import dotenv_values
import time


class Config(object):
    def __init__(self):
        # UDP
        self.udp_base_url = 'https://safe-escarpment-74832.herokuapp.com'

        # Base settings
        self.API_KEY = settings.API_KEY
        self.OKTA_ORG = settings.OKTA_ORG
        self.ISSUER = settings.AUTH_SERVER_ID
        self.CLIENT_ID = settings.CLIENT_ID
        self.CLIENT_SECRET = settings.CLIENT_SECRET

        # Vanity url settings
        self.CUSTOM_LOGIN_URL = settings.CUSTOM_LOGIN_URL
        self.BASE_URL = self.CUSTOM_LOGIN_URL if self.CUSTOM_LOGIN_URL is not None and self.CUSTOM_LOGIN_URL else self.OKTA_ORG

        # Derive the Redirect URIs
        self.URL = settings.URL
        self.DEFAULT_PORT = settings.DEFAULT_PORT
        self.REDIRECT_URI = settings.REDIRECT_URI if settings.REDIRECT_URI is not None and settings.REDIRECT_URI else '[[host]]/oauth2/callback'
        self.AUTH_GROUPADMIN_REDIRECT_URI = '[[host]]/admin'

        self.SCOPES = settings.DEFAULT_SCOPES

        # Social Idp settings
        self.GOOGLE_IDP = settings.GOOGLE_IDP
        self.FB_IDP = settings.FB_IDP
        self.LNKD_IDP = settings.LNKD_IDP
        self.SAML_IDP = settings.SAML_IDP

        # Static
        self.BASE_TITLE = settings.BASE_TITLE if settings.BASE_TITLE is not None and settings.BASE_TITLE else 'API Products Demo'
        self.BASE_ICON = settings.BASE_ICON if settings.BASE_ICON is not None and settings.BASE_ICON else static('/img/okta-brand/logo/okta32x32.png')
        self.DEFAULT_BACKGROUND = static('/img/okta-brand/background/SFbayBridge.jpg')
        if settings.BACKGROUND_IMAGE_DEFAULT and re.match('^/static/', settings.BACKGROUND_IMAGE_DEFAULT):
            self.BACKGROUND_IMAGE = static(re.search('(?<=/static)(.*)', settings.BACKGROUND_IMAGE_DEFAULT).group(0))
        else:
            self.BACKGROUND_IMAGE = settings.BACKGROUND_IMAGE_DEFAULT
        if settings.BACKGROUND_IMAGE_CSS and re.match('^/static/', settings.BACKGROUND_IMAGE_CSS):
            self.BACKGROUND_IMAGE_CSS = static(re.search('(?<=/static)(.*)', settings.BACKGROUND_IMAGE_CSS).group(0))
        else:
            self.BACKGROUND_IMAGE_CSS = settings.BACKGROUND_IMAGE_CSS
        if settings.BACKGROUND_IMAGE_AUTHJS and re.match('^/static/', settings.BACKGROUND_IMAGE_AUTHJS):
            self.BACKGROUND_IMAGE_AUTHJS = static(re.search('(?<=/static)(.*)', settings.BACKGROUND_IMAGE_AUTHJS).group(0))
        else:
            self.BACKGROUND_IMAGE_AUTHJS = settings.BACKGROUND_IMAGE_AUTHJS
        if settings.BACKGROUND_IMAGE_IDP and re.match('^/static/', settings.BACKGROUND_IMAGE_IDP):
            self.BACKGROUND_IMAGE_IDP = static(re.search('(?<=/static)(.*)', settings.BACKGROUND_IMAGE_IDP).group(0))
        else:
            self.BACKGROUND_IMAGE_IDP = settings.BACKGROUND_IMAGE_IDP

        # Option: IDP Discovery setting
        self.IDP_DISCO_PAGE = settings.IDP_DISCO_PAGE
        self.LOGIN_NOPROMPT_BOOKMARK = settings.LOGIN_NOPROMPT_BOOKMARK

        # Impersonation
        self.DELEGATION_SERVICE_ENDPOINT = settings.DELEGATION_SERVICE_ENDPOINT
        self.ALLOW_IMPERSONATION = False

        # Option: Do Impersonation with SAML (Deprecated)
        # self.IMPERSONATION_DEFAULT_VER = 3
        # self.IMPERSONATION_VERSION = settings.IMPERSONATION_VERSION if settings.IMPERSONATION_VERSION and settings.IMPERSONATION_VERSION is not None else self.IMPERSONATION_DEFAULT_VER
        # if (settings.IMPERSONATION_ORG and settings.IMPERSONATION_ORG is not None \
        #     and settings.IMPERSONATION_ORG_AUTH_SERVER_ID and settings.IMPERSONATION_ORG_AUTH_SERVER_ID is not None \
        #     and settings.IMPERSONATION_ORG_OIDC_CLIENT_ID and settings.IMPERSONATION_ORG_OIDC_CLIENT_ID is not None \
        #     and settings.IMPERSONATION_ORG_REDIRECT_IDP_ID and settings.IMPERSONATION_ORG_REDIRECT_IDP_ID is not None \
        #     and settings.IMPERSONATION_SAML_APP_ID and settings.IMPERSONATION_SAML_APP_ID is not None) \
        #     or (settings.IMPERSONATION_V2_ORG and settings.IMPERSONATION_V2_ORG is not None \
        #         and settings.IMPERSONATION_V2_SAML_APP_ID and settings.IMPERSONATION_V2_SAML_APP_ID is not None \
        #         and settings.IMPERSONATION_V2_ORG_API_KEY and settings.IMPERSONATION_V2_ORG_API_KEY is not None \
        #         and settings.IMPERSONATION_V2_SAML_APP_EMBED_LINK and settings.IMPERSONATION_V2_SAML_APP_EMBED_LINK is not None):
        #     self.ALLOW_IMPERSONATION = True

    def get_config(self, request):
        meta = request.META
        scheme = 'http'
        if request.scheme == 'https' or ('HTTP_X_FORWARDED_PROTO' in meta and meta['HTTP_X_FORWARDED_PROTO']) == 'https':
            scheme = 'https'
        http_host = meta['HTTP_HOST']
        print('http_host: {}'.format(http_host))
        http_host_parts = http_host.split('.')
        print('http_host_parts: {}'.format(http_host_parts))
        # meta_http_host = ['zeekhoo', 'super', 'unidemo', 'online']
        subdomain = http_host_parts[0]

        if 'config' in request.session and 'subdomain' in request.session and request.session['subdomain'] == subdomain:
            print('{0}################## already configured {1}###################'.format(time.time(), request.session.session_key))
            config = request.session['config']
        else:
            url = self.URL
            if url is not None:
                host_string = url
                print('host_string1 = {}'.format(host_string))
            else:
                if self.DEFAULT_PORT is not None:
                    host_string = '{0}://{1}:{2}'.format(scheme, request.get_host().split(':')[0], self.DEFAULT_PORT)
                    print('host_string2 = {}'.format(host_string))
                else:
                    host_string = '{0}://{1}'.format(scheme, http_host)
                    print('host_string3 = {}'.format(host_string))

            config = {
                'host': host_string,
                'subdomain': subdomain,
                'base_url': self.BASE_URL,
                'org': self.OKTA_ORG,
                'iss': self.ISSUER,
                'aud': self.CLIENT_ID,
                'scopes': self.SCOPES,
                'url': self.URL,
                'default_port': self.DEFAULT_PORT,
                'redirect_uri': _resolve_redirect_uri(self.REDIRECT_URI, host_string),
                'auth_groupadmin_redirect_uri': _resolve_redirect_uri(self.AUTH_GROUPADMIN_REDIRECT_URI, host_string),
                'google_idp': self.GOOGLE_IDP,
                'fb_idp': self.FB_IDP,
                'lnkd_idp': self.LNKD_IDP,
                'saml_idp': self.SAML_IDP,
                'base_title': self.BASE_TITLE,
                'base_icon': self.BASE_ICON,
                'background': self.BACKGROUND_IMAGE if self.BACKGROUND_IMAGE is not None else self.DEFAULT_BACKGROUND,
                'background_css': self.BACKGROUND_IMAGE_CSS if self.BACKGROUND_IMAGE_CSS is not None else self.DEFAULT_BACKGROUND,
                'background_authjs': self.BACKGROUND_IMAGE_AUTHJS if self.BACKGROUND_IMAGE_AUTHJS is not None else self.DEFAULT_BACKGROUND,
                'background_idp': self.BACKGROUND_IMAGE_IDP if self.BACKGROUND_IMAGE_IDP is not None else self.DEFAULT_BACKGROUND,
                'idp_disco_page': self.IDP_DISCO_PAGE if self.IDP_DISCO_PAGE is not None else 'None',
                'login_noprompt_bookmark': self.LOGIN_NOPROMPT_BOOKMARK,
                'app_permissions_claim': APP_PERMISSIONS_CLAIM,
                'api_permissions_claim': API_PERMISSIONS_CLAIM,
                'allow_impersonation': self.ALLOW_IMPERSONATION,
                'delegation_service_endpoint': self.DELEGATION_SERVICE_ENDPOINT
            }

            try:
                demoapp = http_host_parts[1]
                url = '{0}/api/configs/{1}/{2}/.well-known/default-setting'.format(self.udp_base_url, subdomain, demoapp)
                response = requests.get(url)
                udp = json.loads(response.content)['config']
                # print(udp)
                config.update({
                    'base_url': udp['base_url'].replace('https://', '').replace('http://', ''),
                    'org': udp['base_url'].replace('https://', '').replace('http://', ''),
                    'iss': udp['issuer'].split('/oauth2/')[1],
                    'aud': udp['client_id']
                })
                if 'settings' in udp:
                    udp_settings = udp['settings']
                    if 'org' in udp_settings:
                        config.update({'org': udp_settings['org']})
                    if 'scopes' in udp_settings:
                        config.update({'scopes': udp_settings['scopes']})
                    if 'google_idp' in udp_settings:
                        config.update({'google_idp': udp_settings['google_idp']})
                    if 'fb_idp' in udp_settings:
                        config.update({'fb_idp': udp_settings['fb_idp']})
                    if 'lnkd_idp' in udp_settings:
                        config.update({'lnkd_idp': udp_settings['lnkd_idp']})
                    if 'saml_idp' in udp_settings:
                        config.update({'saml_idp': udp_settings['saml_idp']})
                    if 'base_title' in udp_settings:
                        config.update({'base_title': udp_settings['base_title']})
                    if 'base_icon' in udp_settings:
                        config.update({'base_icon': udp_settings['base_icon']})
                    if 'background' in udp_settings:
                        config.update({'background': udp_settings['background']})
                    if 'background_css' in udp_settings:
                        config.update({'background_css': udp_settings['background_css']})
                    if 'background_authjs' in udp_settings:
                        config.update({'background_authjs': udp_settings['background_authjs']})
                    if 'background_idp' in udp_settings:
                        config.update({'background_idp': udp_settings['background_idp']})
                    if 'idp_disco_page' in udp_settings:
                        config.update({'idp_disco_page': udp_settings['idp_disco_page']})
                    else:
                        client = AppsClient('https://{}'.format(config['org']),
                                            self.get_api_key(request),
                                            config['aud'])
                        config.update({'idp_disco_page': client.get_login_disco_url()})

                    if 'login_noprompt_bookmark' in udp_settings:
                        config.update({'login_noprompt_bookmark': udp_settings['login_noprompt_bookmark']})
                    if 'delegation_service_endpoint' in udp_settings:
                        config.update({'delegation_service_endpoint': udp_settings['delegation_service_endpoint']})

            except Exception as e:
                print('Exception in get_config: {}'.format(e))

            print('{0}################## INIT CONFIG {1}###################'.format(time.time(), request.session.session_key))
            request.session['config'] = config
            request.session['subdomain'] = subdomain
        return config

    def get_api_key(self, request):
        try:
            meta = request.META
            meta_http_host = meta['HTTP_HOST'].split('.')
            subdomain = meta_http_host[0]
            demoapp = meta_http_host[1]
            url = '{0}/api/configs/{1}/{2}/secret'.format(self.udp_base_url, subdomain, demoapp)
            response = requests.get(url)
            fileLike = StringIO(str(response.content, 'utf-8'))
            fileLike.seek(0)
            parsed = dotenv_values(stream=fileLike)
            return parsed['OKTA_API_TOKEN']
        except Exception as e:
            print('Exception in get_api_key: {}'.format(e))
        return self.API_KEY

    def get_client_secret(self, request):
        try:
            meta = request.META
            meta_http_host = meta['HTTP_HOST'].split('.')
            subdomain = meta_http_host[0]
            demoapp = meta_http_host[1]
            url = '{0}/api/configs/{1}/{2}/secret'.format(self.udp_base_url, subdomain, demoapp)
            response = requests.get(url)
            fileLike = StringIO(str(response.content, 'utf-8'))
            fileLike.seek(0)
            parsed = dotenv_values(stream=fileLike)
            return parsed['CLIENT_SECRET']
        except Exception as e:
            print('Exception in get_client_secret: {}'.format(e))
        return self.CLIENT_SECRET


def _resolve_redirect_uri(redirect_uri, host):
    return redirect_uri\
        .replace('[[', '{') \
        .replace(']]', '}') \
        .format(host=host)
