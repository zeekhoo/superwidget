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


authClient.token.getWithRedirect({
    responseType: ['code'],
    scopes: [[scopes]]
});