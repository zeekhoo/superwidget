var redirect = 'https://[[base_url]]/oauth2/v1/authorize'
    + '?response_type=token'
    + '&client_id=[[aud]]'
    + '&scope=okta.users.read'
    + '&state=foo'
    + '&nonce=foo'
    + '&redirect_uri=[[auth_groupadmin_redirect]]'

window.location.href = redirect;
