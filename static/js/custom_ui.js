function do_login(un, pw) {
    var authClient = new OktaAuth({
        url: 'https://[[org]]',
        clientId: '[[aud]]',
        redirectUri: '[[redirect]]',
        issuer: 'https://[[org]]/oauth2/[[iss]]'
    });

    authClient.signIn({
        username: un,
        password: pw
    })
    .then(function(transaction) {
        if (transaction.status === 'SUCCESS') {
            // Step #1: get sessionToken
            console.log('sessionToken = ', transaction.sessionToken);

            // Step #2: retrieving a session cookie via OpenID Connect Authorization Endpoint
            // Requires the user be authenticated already (i.e. the transaction.sessionToken exists. See Step #1)
            // Uses response_mode=form_post: This will POST authorization_code and state to the redirectUri
            authClient.token.getWithRedirect({
                responseType: 'code',
                sessionToken: transaction.sessionToken,
                scopes: [[scopes]],
            });
        } else {
            throw 'We cannot handle the ' + transaction.status + ' status';
        }
    })
    .fail(function(err) {
        console.error(err);
    });
}


