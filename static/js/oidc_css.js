var oktaSignIn = new OktaSignIn({
    baseUrl: 'https://[[org]]',
    clientId: '[[aud]]',
    redirectUri: '[[redirect]]',
    authParams: {
        issuer: 'https://[[org]]/oauth2/[[iss]]',
        responseType: ['id_token', 'token'],
        scopes: [[scopes]],
    },
    features: {
        router: true,
        registration: false,
        rememberMe: true,
        //multiOptionalFactorEnroll: true,
        //selfServiceUnlock: true,
        //smsRecovery: true,
    	//callRecovery: true,
    },
    logo: '/static/img/gear_half.png', //more:[logo_widgico.png, gear_logo.png, gear_half.png]
    language: 'en', //more: [fr, de, es, ja, zh-CN] Full list here: https://github.com/okta/okta-signin-widget#language-and-text
    i18n: {
        'en': {
            'primaryauth.title': 'Sign In',
            'primaryauth.submit': 'Sign In',
            //Full list here: https://github.com/okta/okta-signin-widget/blob/master/packages/@okta/i18n/dist/properties/login.properties
        }
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

