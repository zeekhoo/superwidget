from django.urls import path, re_path
from .api import *
from .views import *

urlpatterns = [
    # home
    re_path(r'^$', view_home, name='home'),
    path('login-noprompt/', view_login_auto, name='login_noprompt'),
    path('auth-groupadmin/', view_auth_groupadmin, name='auth_groupadmin'),

    # login
    path('login/', view_login, name='login_default'),
    path('logout/', view_logout, name='logout'),

    re_path(r'^signin/reset-password/(?P<recoveryToken>.*)', view_login, name='reset_password'),
    re_path(r'^signin/recovery-question/(?P<recoveryToken>.*)', view_login, name='admin_reset_password'),

    # profile page
    path('profile/', view_profile, name='profile'),
    # re_path(r'^edit-profile/', edit_profile, name='edit-profile'), TODO: Implement

    # admin/crud
    path('admin/', view_admin, name='admin'),  # FIXME: Protect route
    path('list-users/', list_users, name='list_users'),
    path('list-user/', list_user, name='list_user'),
    path('add-users', add_users, name='add_users'),
    path('update-user', update_user, name='update_user'),
    path('add-group', add_group, name='add_group'),
    path('list-groups/', list_groups, name='list_groups'),
    path('list-group/', get_group, name='list_group'),  # TODO: unused api. please cleanup
    path('list-perms/', list_perms, name='list_perms'),
    path('app-schema', app_schema, name='app_schema'),
    path('update-perm', update_perm, name='update_perm'),

    # impersonation (Deprecated)
    # url(r'^set-name-id', setNameId, name='set_name_id'),
    # url(r'^login-delegate', login_delegate, name='login_delegate'),

    # impersonation
    path('delegate-init', delegate_init, name='delegate_init'),

    # alternate login pages
    path('login-css/', view_login_css, name='login_css'),
    path('for-okta-hosted/', okta_hosted_login, name='login_okta_hosted'),
    path('login-idp/', view_login_idp, name='login_idp'),
    path('login-disco/', view_login_disco, name='login_idp_disco'),
    path('login-form/', view_login_custom, name='login_custom'),
    path('login-custom-demo/', view_login_custom_demo, name='login_custom_demo'),

    # auth code postback
    path('oauth2/callback', oauth2_post, name='oauth2_post'),
    path('oauth/callback', oauth2_callback, name='oauth2_callback'),

    # callbacks
    path('process-creds', process_creds, name='process_creds'),

    # registration examples
    path('register/', registration_view, name='register_user'),
    path('register2/', registration_view2, name='register_user2'),
    path('success/', registration_success, name='registration_success'),
    path('success2/', registration_success2, name='registration_success2'),
    re_path(r'^activate/(?P<slug>.*)/$', activation_view, name='activate_user'),
    path('activate/', activation_wo_token_view, name='activate_user2'),

    # error pages
    path('not-authenticated/', not_authenticated, name='not_authenticated'),
    path('not-authorized/', not_authorized, name='not_authorized'),

    # health check
    path('health/', health_check, name='health_check'),

    # Sensitive Access- Step-up MFA secured.
    path('sensitive_operations/', view_sensitive_operations, name='sensitive_operations'), # FIXME: Protect this route
    path('transfer', transfer_money, name='transfer_money'),
]

