var oktaSignIn = new OktaSignIn({
    baseUrl: 'https://[[org]]',
    clientId: '[[aud]]',
    redirectUri: '[[redirect]]',
    features: {
        rememberMe: true,
        smsRecovery: true,
        callRecovery: false,
        selfServiceUnlock: true,
        router: true,
        registration: true,
    },
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