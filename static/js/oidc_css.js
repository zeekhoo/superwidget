var base_url = 'https://' + org;
var issuer = base_url + '/oauth2/' + iss;
var client_id = aud;
var redirect_uri = 'http://localhost:8000/oauth2/postback';
var scp = ['openid', 'profile', 'email', 'address', 'phone', 'offline_access'];
scp.push.apply(scp, more);

var oktaSignIn = new OktaSignIn({
    baseUrl: base_url,
    logo: 'https://developer.okta.com/sites/all/themes/developer/media/logo.svg',
    features: {
        rememberMe: true,
        multiOptionalFactorEnroll: true,
        smsRecovery: true,
        callRecovery: false,
        selfServiceUnlock: true,
    },
    //language and localization settings
    language: 'en',
    i18n: {
        'en': {
            'primaryauth.username.placeholder': 'Signin with your Email',
            'primaryauth.submit': 'Access My Account',
            'needhelp': 'Click for more Options',
            'password.forgot.email.or.username.placeholder': 'Enter your email, then click below',
        }
    },
    //OpenIDConnect, OAuth2 settings
    clientId: client_id,
    redirectUri: redirect_uri,
    authParams: {
        issuer: issuer,
        responseType: ['id_token', 'token'],
        scopes: scp,
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
