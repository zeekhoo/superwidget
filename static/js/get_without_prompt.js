var oktaSignIn = new OktaSignIn({
    baseUrl: 'https://[[base_url]]',
    clientId: '[[aud]]',
    redirectUri: '[[redirect]]',
    authParams: {
        issuer: 'https://[[base_url]]/oauth2/[[iss]]',
        pkce: false
    }
});
var authClient = oktaSignIn.authClient;

authClient.session.exists()
.then(function(exists) {
    if (exists) {
        var scp = [[scopes]];

        authClient.tokenManager.get('accessToken')
        .then(function(token) {
            if (token) {
                scp = token.scopes;
            }
            console.log(scp);
            authClient.token.getWithoutPrompt({
                responseType: ['id_token', 'token'],
                scopes: scp,
            })
            .then(function(res){
                if (res.tokens) {
                    authClient.tokenManager.add('accessToken', res.tokens.accessToken);
                    authClient.tokenManager.add('idToken', res.tokens.idToken);
                    login(res.tokens.idToken, res.tokens.accessToken);
                }
            });
        })
        .catch(function(err){
            console.log(err);
        });
    } else {
        console.log('not logged in');
    }
});
