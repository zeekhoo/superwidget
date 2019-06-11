from django.contrib.staticfiles.templatetags.staticfiles import static
from .authx import *
import re

DEFAULT_PORT = settings.DEFAULT_PORT if settings.DEFAULT_PORT is not None and settings.DEFAULT_PORT else '8000'


class Config(object):
    def __init__(self):
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
        self.REDIRECT_URI = settings.REDIRECT_URI if settings.REDIRECT_URI is not None and settings.REDIRECT_URI else 'http://localhost:{}/oauth2/callback'.format(DEFAULT_PORT)
        self.AUTH_GROUPADMIN_REDIRECT_URI = 'http://localhost:{}/admin'.format(DEFAULT_PORT)

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
            self.BACKGROUND_IMAGE = static(settings.BACKGROUND_IMAGE_DEFAULT)
        if settings.BACKGROUND_IMAGE_CSS and re.match('^/static/', settings.BACKGROUND_IMAGE_CSS):
            self.BACKGROUND_IMAGE_CSS = static(re.search('(?<=/static)(.*)', settings.BACKGROUND_IMAGE_CSS).group(0))
        else:
            self.BACKGROUND_IMAGE_CSS = static(settings.BACKGROUND_IMAGE_CSS)
        if settings.BACKGROUND_IMAGE_AUTHJS and re.match('^/static/', settings.BACKGROUND_IMAGE_AUTHJS):
            self.BACKGROUND_IMAGE_AUTHJS = static(re.search('(?<=/static)(.*)', settings.BACKGROUND_IMAGE_AUTHJS).group(0))
        else:
            self.BACKGROUND_IMAGE_AUTHJS = static(settings.BACKGROUND_IMAGE_AUTHJS)
        if settings.BACKGROUND_IMAGE_IDP and re.match('^/static/', settings.BACKGROUND_IMAGE_IDP):
            self.BACKGROUND_IMAGE_IDP = static(re.search('(?<=/static)(.*)', settings.BACKGROUND_IMAGE_IDP).group(0))
        else:
            self.BACKGROUND_IMAGE_IDP = static(settings.BACKGROUND_IMAGE_IDP)

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

    def get_config(self):
        config = {
            "base_url": self.BASE_URL,
            "org": self.OKTA_ORG,
            "iss": self.ISSUER,
            "aud": self.CLIENT_ID,
            "scopes": self.SCOPES,
            "redirect_uri": self.REDIRECT_URI,
            "auth_groupadmin_redirect_uri": self.AUTH_GROUPADMIN_REDIRECT_URI,
            "google_idp": self.GOOGLE_IDP,
            "fb_idp": self.FB_IDP,
            "lnkd_idp": self.LNKD_IDP,
            "saml_idp": self.SAML_IDP,
            "base_title": self.BASE_TITLE,
            "base_icon": self.BASE_ICON,
            "background": self.BACKGROUND_IMAGE if self.BACKGROUND_IMAGE is not None else self.DEFAULT_BACKGROUND,
            "background_css": self.BACKGROUND_IMAGE_CSS if self.BACKGROUND_IMAGE_CSS is not None else self.DEFAULT_BACKGROUND,
            "background_authjs": self.BACKGROUND_IMAGE_AUTHJS if self.BACKGROUND_IMAGE_AUTHJS is not None else self.DEFAULT_BACKGROUND,
            "background_idp": self.BACKGROUND_IMAGE_IDP if self.BACKGROUND_IMAGE_IDP is not None else self.DEFAULT_BACKGROUND,
            "idp_disco_page": self.IDP_DISCO_PAGE if self.IDP_DISCO_PAGE is not None else 'None',
            "login_noprompt_bookmark": self.LOGIN_NOPROMPT_BOOKMARK,
            "app_permissions_claim": APP_PERMISSIONS_CLAIM,
            "api_permissions_claim": API_PERMISSIONS_CLAIM,
            "allow_impersonation": self.ALLOW_IMPERSONATION,
            "delegation_service_endpoint": self.DELEGATION_SERVICE_ENDPOINT
        }
        return config

    def get_api_key(self):
        return self.API_KEY

    def get_client_secret(self):
        return self.CLIENT_SECRET
