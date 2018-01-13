var oktaSignIn = new OktaSignIn({
    baseUrl: 'https://[[org]]',
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
            'primaryauth.submit': 'Sign In',
            'primaryauth.username.placeholder': 'Username',
            'needhelp': 'Need Help?',
            'password.forgot.email.or.username.placeholder': 'Enter your email, then click below',
        }
    },
    //OpenIDConnect, OAuth2 settings
    clientId: '[[aud]]',
    redirectUri: '[[redirect]]',
    authParams: {
        issuer: 'https://[[org]]/oauth2/[[iss]]',
        responseType: ['id_token', 'token'],
        scopes: [[scopes]],
    },
});

oktaSignIn.renderEl(
    {el: '#okta-login-container'},
    function (res) {
        var key = '';
        if (res[0]) {
            key = Object.keys(res[0])[0];
            oktaSignIn.tokenManager.add(key, res[0]);
        }
        if (res[1]) {
            key = Object.keys(res[1])[0];
            oktaSignIn.tokenManager.add(key, res[1]);
        }
        if (res.status === 'SUCCESS') {
            get_profile(key, oktaSignIn.tokenManager.get(key));
        }
    }
);