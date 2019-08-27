from django.conf.urls import url
from .api import *
from .views import *


urlpatterns = [
    url(r'^edit-profile/', edit_profile, name='edit-profile'),

    # home
    url(r'^$', view_home, name='home'),
    url(r'^tokens$', view_tokens, name='tokens'),
    url(r'^login$', view_login, name='login_default'),
    url(r'^signin/reset-password/(?P<recoveryToken>.*)', view_login, name='reset_password'),
    url(r'^signin/recovery-question/(?P<recoveryToken>.*)', view_login, name='admin_reset_password'),
    url(r'^login-noprompt', view_login_auto, name='login_noprompt'),
    url(r'^auth-groupadmin', view_auth_groupadmin, name='auth_groupadmin'),

    # login
    url(r'^logout$', view_logout, name='logout'),
    url(r'^clear-session', clear_session, name='clear_session'),

    # profile page
    url(r'^profile$', view_profile, name='profile'),

    # admin/crud
    url(r'^admin/', view_admin, name='admin'),
    url(r'^list-users', list_users, name='list_users'),
    url(r'^list-user', list_user, name='list_user'),
    url(r'^add-users', add_users, name='add_users'),
    url(r'^update-user', update_user, name='update_user'),
    url(r'^add-group', add_group, name='add_group'),
    url(r'^list-groups', list_groups, name='list_groups'),
    url(r'^list-group', get_group, name='list_group'),  # TODO: unused api. please cleanup
    url(r'^list-perms', list_perms, name='list_perms'),
    url(r'^app-schema', app_schema, name='app_schema'),
    url(r'^update-perm', update_perm, name='update_perm'),

    # impersonation (Deprecated)
    # url(r'^set-name-id', setNameId, name='set_name_id'),
    # url(r'^login-delegate', login_delegate, name='login_delegate'),

    # impersonation
    url(r'^delegate-init', delegate_init, name='delegate_init'),

    # alternate login pages
    url(r'^login-css$', view_login_css, name='login_css'),
    url(r'^for-okta-hosted$', okta_hosted_login, name='login_okta_hosted'),
    url(r'^login-idp$', view_login_idp, name='login_idp'),
    url(r'^login-disco', view_login_disco, name='login_idp_disco'),
    url(r'^login-form$', view_login_custom, name='login_custom'),
    url(r'^login-custom-demo$', view_login_custom_demo, name='login_custom_demo'),

    # auth code postback
    url(r'^oauth2/callback', oauth2_post, name='oauth2_post'),
    url(r'^oauth/callback', oauth2_callback, name='oauth2_callback'),

    # callbacks
    url(r'^process-creds', process_creds, name='process_creds'),

    # registration examples
    url(r'^register/', registration_view, name='register_user'),
    url(r'^register2/', registration_view2, name='register_user2'),
    url(r'^success/$', registration_success, name='registration_success'),
    url(r'^success2/$', registration_success2, name='registration_success2'),
    url(r'^activate/(?P<slug>.*)/$', activation_view, name='activate_user'),
    url(r'^activate/$', activation_wo_token_view, name='activate_user2'),

    # error pages
    url(r'^not-authenticated/$', not_authenticated, name='not_authenticated'),
    url(r'^not-authorized/$', not_authorized, name='not_authorized'),

    # health check
    url(r'^health/$', health_check, name='health_check'),
    url(r'^hello-redis/$', hello_redis, name='hello_redis'),
]
