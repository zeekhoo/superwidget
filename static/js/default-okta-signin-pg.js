var config = {
    url: 'https://[[org]]',
    clientId: '[[aud]]',
    redirectUri: '[[redirect]]',
    issuer: 'https://[[org]]/oauth2/[[iss]]'
};
var authClient = new OktaAuth(config);

authClient.token.getWithRedirect({
    responseType: ['code'],
    scopes: [[scopes]]
});