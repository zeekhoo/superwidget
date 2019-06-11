var org = 'https://[[org]]';

var options = {
    url: org,
    clientId: '[[aud]]',
    redirectUri: '[[redirect]]',
    issuer: org + '/oauth2/[[iss]]'
}

var authClient = new OktaAuth(options);

authClient.session.exists()
.then(function(exists) {
    if (exists) {
        var scp = [[scopes]];

        if (authClient.tokenManager.get('accessToken')) {
            var access_token_str = authClient.tokenManager.get('accessToken').accessToken;
            var access_token = JSON.parse(window.atob(access_token_str.split('.')[1]));
            scp = access_token.scp;
        }

        authClient.token.getWithoutPrompt({
            responseType: ['id_token', 'token'],
            scopes: scp,
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
    login(authClient.tokenManager.get('idToken'), authClient.tokenManager.get('accessToken'));
}