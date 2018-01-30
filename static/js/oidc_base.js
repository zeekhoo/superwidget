var oktaSignIn = new OktaSignIn({
    baseUrl: 'https://[[org]]',
    logo: '',    //e.g. /static/img/logo_widgico.png

    //------------OpenIDConnect, OAuth2 settings----------------
    clientId: '[[aud]]',
    redirectUri: '[[redirect]]',
    authParams: {
        issuer: 'https://[[org]]/oauth2/[[iss]]',
        responseType: ['id_token', 'token'],
        scopes: [[scopes]],
    },
    //-----------------MORE OPTIONS:-----------------
    //[multiOptionalFactorEnroll, smsRecovery, callRecovery, selfServiceUnlock, hideSignOutLinkInMFA, registration]
    //-----------------------------------------------
    features: {
        router: true,
        rememberMe: false,
        selfServiceUnlock: false,
    },
    //------------LANGUAGE and LOCALIZATION settings-----------------------------------------------------------------------------
    //Example tags: [primaryauth.username.placeholder,  primaryauth.password.placeholder, needhelp, etc.]
    //Full list here: https://github.com/okta/okta-signin-widget/blob/master/packages/@okta/i18n/dist/properties/login.properties
    //---------------------------------------------------------------------------------------------------------------------------
    language: 'en',
    i18n: {
        'en': {
            'primaryauth.title': 'Sign In',
            'primaryauth.submit': 'Sign In',
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

