var base_url = 'https://' + org;
var issuer = base_url + '/oauth2/' + iss;
var client_id = aud;
var redirect_uri = 'http://localhost:8000/oauth2/postback';


var config = {
    url: base_url,
    clientId: client_id,
    redirectUri: redirect_uri,
    issuer: issuer,
};
var authClient = new OktaAuth(config);

authClient.token.getWithRedirect({
    responseType: ['token'],
    responseMode: 'form_post',
    scopes: [
        'openid', 'profile', 'email', 'address', 'phone'
        ,'com.zeek.p1.resource1.admin'
        ,'com.zeek.p1.resource1.user'
    ],
});