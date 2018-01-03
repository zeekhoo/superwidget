"""okta_widget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from .views import not_authenticated
from .views import view_home, view_tokens
from .views import view_login, view_logout, view_profile
from .views import oauth2_post, oauth2_callback, registration_view, registration_success
from .views import view_login_css, customized_okta_hosted, view_login_raas, view_login_idp
from .views import view_login_baybridge, view_login_brooklynbridge
from .views import view_login_custom
from .views import view_app_b
from .views import auth_broker, sessions_broker
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # home
    url(r'^$', view_home, name='home'),
    url(r'^tokens$', view_tokens, name='tokens'),
    url(r'^login$', view_login, name='login'),
    url(r'^logout$', view_logout, name='logout'),


    # profile page
    url(r'^profile$', view_profile, name='profile'),

    # alternate login pages
    url(r'^login-css$', view_login_css, name='login_css'),
    url(r'^for-okta-hosted$', customized_okta_hosted, name='customized_okta_hosted'),
    url(r'^login-raas$', view_login_raas, name='login_raas'),
    url(r'^login-idp$', view_login_idp, name='login_idp'),
    url(r'^app_b$', view_app_b, name='app_b'),
    url(r'^login-form$', view_login_custom, name='login_custom'),

    url(r'^login-baybridge$', view_login_baybridge, name='login_baybridge'),
    url(r'^login-brooklynbridge$', view_login_brooklynbridge, name='login_brooklynbridge'),

    # okta proxy
    url(r'^broker/api/v1/sessions/me$', sessions_broker, name='okta_session'),
    url(r'^broker/api/v1/authn$', auth_broker, name='okta_auth'),

    # auth code postback
    url(r'^oauth2/postback', oauth2_post, name='oauth2_post'),
    url(r'^oauth/callback', oauth2_callback, name='oauth2_callback'),

    url(r'^register/', registration_view, name='register_user'),
    url(r'^success/$', registration_success, name='registration_success'),

    url(r'^not-authenticated/$', not_authenticated, name='not_authenticated'),

]

# urlpatterns += staticfiles_urlpatterns()
