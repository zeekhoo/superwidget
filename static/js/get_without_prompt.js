var authClient = new OktaAuth({
    url: 'https://[[org]]',
    clientId: '[[aud]]',
    redirectUri: '[[redirect]]',
    issuer: 'https://[[org]]/oauth2/[[iss]]'
});

authClient.session.exists()
.then(function(exists) {
    if (exists) {
        authClient.token.getWithoutPrompt({
            responseType: ['id_token', 'token'],
            scopes: [[scopes]],
        })
        .then(function(tokens){
            showApp(tokens);
        })
        .then(function(err){
            console.log(err);
        })
    } else {
        console.log('not logged in');
    }
});

function showApp(res) {
    var key = '';
    if (res[0]) {
        key = Object.keys(res[0])[0];
        authClient.tokenManager.add(key, res[0]);
    }
    if (res[1]) {
        key = Object.keys(res[1])[0];
        authClient.tokenManager.add(key, res[1]);
    }
    post_tokens(oktaSignIn.tokenManager.get('idToken'), oktaSignIn.tokenManager.get('accessToken'));
    get_profile(key, authClient.tokenManager.get(key));
}
