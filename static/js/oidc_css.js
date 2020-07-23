var oktaSignIn = new OktaSignIn({
    baseUrl: 'https://[[base_url]]',
    clientId: '[[aud]]',
    redirectUri: '[[redirect]]',
    authParams: {
        issuer: 'https://[[base_url]]/oauth2/[[iss]]',
        responseType: ['code'],
        scopes: [[scopes]],
        pkce: false
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
    logo: '[[base_icon]]', //more:[logo_widgico.png, gear_logo.png, gear_half.png]
    language: 'en', //more: [fr, de, es, ja, zh-CN] Full list here: https://github.com/okta/okta-signin-widget#language-and-text
    i18n: {
        'en': {
            'primaryauth.title': 'Sign In',
            'primaryauth.submit': 'Sign In',
            //Full list here: https://github.com/okta/okta-signin-widget/blob/master/packages/@okta/i18n/src/properties/login.properties
        }
    },
});
oktaSignIn.renderEl( //Caution editing this section as you may break the demo.
    {el: '#okta-login-container'},
    function (res) {
        var key = '';
        if (res.tokens) {
            oktaSignIn.authClient.tokenManager.add('accessToken', res.tokens.accessToken);
            oktaSignIn.authClient.tokenManager.add('idToken', res.tokens.idToken);
            if (res.status === 'SUCCESS') {
                login(res.tokens.idToken, res.tokens.accessToken);
            }
        }
    }
);