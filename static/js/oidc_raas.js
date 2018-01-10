var base_url = 'https://' + org;
var issuer = base_url + '/oauth2/' + iss;
var client_id = aud;
var redirect_uri = 'http://localhost:8000/oauth2/postback';

var oktaSignIn = new OktaSignIn({
    baseUrl: base_url,
    clientId: client_id,
    redirectUri: redirect_uri,
    features: {
        router: true,
        registration: true,
    },
    authParams: {
        issuer: issuer,
        responseType: ['id_token', 'token'],
        scopes: [
            'openid', 'profile', 'email', 'address', 'phone', 'offline_access',
            'com.zeek.p1.resource1.admin',
            'com.zeek.p1.resource1.user'
        ],
    },
});
oktaSignIn.session.get(function (res) {
    oktaSignIn.renderEl(
        {el: '#okta-login-container'},
        function (res) {
            oktaSignIn.tokenManager.add('id_token', res[0]);
            oktaSignIn.tokenManager.add('access_token', res[1]);
            if (res.status === 'SUCCESS') {
                get_profile(oktaSignIn.tokenManager.get('access_token').accessToken);
            }
        },
        function error(err) {
            console.log('Unexpected error authenticating user: %o', err);
        }
    );
});
