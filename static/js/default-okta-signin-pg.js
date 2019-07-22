var config = {
    url: 'https://[[base_url]]',
    clientId: '[[aud]]',
    redirectUri: '[[redirect]]',
    issuer: 'https://[[base_url]]/oauth2/[[iss]]'
};
var authClient = new OktaAuth(config);

authClient.token.getWithRedirect({
    responseType: ['code'],
    scopes: [[scopes]]
});