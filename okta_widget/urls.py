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
from .views import not_authorized
from .views import view_home, view_tokens, view_admin, view_debug
from .views import list_users, list_user, setNameId, login_delegate, add_users, update_user
from .views import app_schema, list_groups, list_perms, get_group, update_perm, add_group
from .views import process_creds
from .views import view_login, view_logout, view_profile, edit_profile
from .views import oauth2_post, oauth2_callback
from .views import registration_view, registration_view2, \
    registration_success, registration_success2, \
    activation_view, activation_wo_token_view
from .views import view_login_css, okta_hosted_login, view_login_idp, view_login_disco
from .views import view_login_custom


# from .views import auth_broker, sessions_broker
# from .views import hellovue
# from .views import view_login_baybridge, view_login_brooklynbridge
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', view_admin, name='admin'),
    url(r'^debug/', view_debug, name='debug'),
    url(r'^edit-profile/', edit_profile, name='edit-profile'),

    # home
    url(r'^$', view_home, name='home'),
    url(r'^tokens$', view_tokens, name='tokens'),
    url(r'^login$', view_login, name='login'),
    url(r'^logout$', view_logout, name='logout'),


    # profile page
    url(r'^profile$', view_profile, name='profile'),

    # impersonation
    url(r'^list-users', list_users, name='list_users'),
    url(r'^list-user', list_user, name='list_user'),
    url(r'^add-users', add_users, name='add_users'),
    url(r'^update-user', update_user, name='update_user'),
    url(r'^add-group', add_group, name='add_group'),
    url(r'^list-groups', list_groups, name='list_groups'),
    url(r'^list-group', get_group, name='list_group'),
    url(r'^list-perms', list_perms, name='list_perms'),
    url(r'^app-schema', app_schema, name='app_schema'),
    url(r'^update-perm', update_perm, name='update_perm'),
    url(r'^set-name-id', setNameId, name='set_name_id'),
    url(r'^login-delegate', login_delegate, name='login_delegate'),
    # url(r'^proxy-callback', proxy_callback, name='proxy_callback'),


    # callbacks
    url(r'^process-creds', process_creds, name='process_creds'),

    # alternate login pages
    url(r'^login-css$', view_login_css, name='login_css'),
    url(r'^for-okta-hosted$', okta_hosted_login, name='okta_hosted_login'),
    # url(r'^login-raas$', view_login_raas, name='login_raas'),
    url(r'^login-idp$', view_login_idp, name='login_idp'),
    url(r'^login-disco$', view_login_disco, name='login_idp_disco'),
    url(r'^login-form$', view_login_custom, name='login_custom'),


    # auth code postback
    url(r'^oauth2/callback', oauth2_post, name='oauth2_post'),
    url(r'^oauth/callback', oauth2_callback, name='oauth2_callback'),

    url(r'^register/', registration_view, name='register_user'),
    url(r'^register2/', registration_view2, name='register_user2'),
    url(r'^success/$', registration_success, name='registration_success'),
    url(r'^success2/$', registration_success2, name='registration_success2'),
    url(r'^activate/(?P<slug>.*)/$', activation_view, name='activate_user'),
    url(r'^activate/$', activation_wo_token_view, name='activate_user2'),

    url(r'^not-authenticated/$', not_authenticated, name='not_authenticated'),
    url(r'^not-authorized/$', not_authorized, name='not_authorized'),
    # okta proxy
    # url(r'^broker/api/v1/sessions/me$', sessions_broker, name='okta_session'),
    # url(r'^broker/api/v1/authn$', auth_broker, name='okta_auth'),

    # url(r'^login-baybridge$', view_login_baybridge, name='login_baybridge'),
    # url(r'^login-brooklynbridge$', view_login_brooklynbridge, name='login_brooklynbridge'),
    # url(r'^hellovue/$', hellovue, name='hellovue'),
]

# urlpatterns += staticfiles_urlpatterns()
