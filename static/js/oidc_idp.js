var oktaSignIn = new OktaSignIn({
    baseUrl: 'https://[[base_url]]',
    clientId: '[[aud]]',
    redirectUri: '[[redirect]]',
    authParams: {
        issuer: 'https://[[base_url]]/oauth2/[[iss]]',
        display: 'popup',
        responseType: ['code'],
        scopes: [[scopes]],
        pkce: false
    },
    idps: [[idps]],
    customButtons: [[btns]],
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
