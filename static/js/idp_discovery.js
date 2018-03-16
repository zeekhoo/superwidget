var oktaSignIn = new OktaSignIn({
    baseUrl: 'https://[[org]]',
    idpDiscovery: {
        requestContext: '/'
    },
    features: {
        idpDiscovery: true,
    },
});

oktaSignIn.session.get(function(res) {
    if (res.status==='ACTIVE') {
        var authClient = new OktaAuth({
            url: 'https://[[org]]',
            clientId: '[[aud]]',
            redirectUri: '[[redirect]]',
            issuer: 'https://[[org]]/oauth2/[[iss]]'
        });

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
        oktaSignIn.renderEl(
            {el: '#okta-login-container'},
            function (res) {
                if (res.status === 'IDP_DISCOVERY') {
                    res.idpDiscovery.redirectToIdp('[[idp_disco]]');
                    return;
                }
                if (res.status === 'SUCCESS') {
                    showApp(res);
                }
            }
        );
    }
});


function showApp(res) {
    var key = '';
    if (res[0]) {
        key = Object.keys(res[0])[0];
        oktaSignIn.tokenManager.add(key, res[0]);
    }
    if (res[1]) {
        key = Object.keys(res[1])[0];
        oktaSignIn.tokenManager.add(key, res[1]);
    }
    get_profile(key, oktaSignIn.tokenManager.get(key));
}