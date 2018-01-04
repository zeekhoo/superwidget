var baseUrl = 'https://' + org;
var issuer = baseUrl + '/oauth2/' + iss;
var client_id = aud;
var redirect_uri = 'http://localhost:8000/oauth2/postback';


var config = {
    url: baseUrl,
    clientId: client_id,
    redirectUri: redirect_uri,
    issuer: issuer,
};
var authClient = new OktaAuth(config);

authClient.token.getWithRedirect({
    responseType: 'code',
    responseMode: 'form_post',
    scopes: [
        'openid', 'profile', 'email', 'address', 'phone',
        'com.zeek.p1.resource1.admin',
        'com.zeek.p1.resource1.user'
    ],
});