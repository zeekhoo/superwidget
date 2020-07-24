function do_login(un, pw) {
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
    authClient.signIn({
        username: un,
        password: pw
    })
    .then(function(transaction) {
        if (transaction.status === 'SUCCESS') {
            // Step #1: get sessionToken
            var sessionToken = transaction.sessionToken;

            // Step #2: retrieving a session cookie via OpenID Connect Authorization Endpoint
            // Requires the user be authenticated already (i.e. the transaction.sessionToken exists. See Step #1)
            // Uses response_mode=form_post: This will POST authorization_code and state to the redirectUri
            authClient.token.getWithRedirect({
                responseType: 'code',
                sessionToken: sessionToken,
                scopes: [[scopes]],
            });
        } else {
            throw 'We cannot handle the ' + transaction.status + ' status';
        }
    })
    .catch(function(err) {
        console.error(err);
    });
}


