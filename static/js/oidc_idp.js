var base_url = 'https://' + org;             //e.g. 'https://login.alwaysaasure.com';
var issuer = base_url + '/oauth2/' + iss;    //e.g. 'https://login.alwaysaasure.com/oauth2/default';
var client_id = aud;                         //e.g. '0oadbg08aaYtrMlRC0h7'
var redirect_uri = 'http://localhost:8000/oauth2/postback';
var scp = ['openid', 'profile', 'email', 'address', 'phone', 'offline_access'];
scp.push.apply(scp, more);

var idp_id = saml_idp;
var goo_id = goog;
var fb_id = fb;
var lnkd_id = lnkd;

var idps = [];
if (goo_id != 'None') {idps.push({type: 'GOOGLE', id: goo_id});}
if (fb_id != 'None') {idps.push({type: 'FACEBOOK', id: fb_id});}
if (lnkd_id != 'None') {idps.push({type: 'LINKEDIN', id: lnkd_id});}

var btns = [];
if (idp_id != 'None') {
    btns.push({
        title: 'Login SAML Idp',
        className: 'btn-customAuth',
        click: function() {
            var link =  issuer + '/v1/authorize'
                        + '?response_type=id_token+token'
                        + '&response_mode=form_post'
                        + '&client_id=' + client_id
                        + '&scope=openid+email+profile'
                        + '&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Foauth2%2Fpostback'
                        + '&state=foo'
                        + '&nonce=foo'
                        + '&idp=' + idp_id
            window.location.href = link;
        }
    });
}

var oktaSignIn = new OktaSignIn({
    baseUrl: base_url,
    clientId: client_id,
    redirectUri: redirect_uri,
    authParams: {
        issuer: issuer,
        display: 'popup',
        responseType: ['id_token', 'token'],
        scopes: scp,
    },
    idps: idps,
    customButtons: btns,
    features: {
        rememberMe: true,
        multiOptionalFactorEnroll: true,
        smsRecovery: true,
        callRecovery: false,
        selfServiceUnlock: true,
    }
});

oktaSignIn.session.get(function (res) {
    oktaSignIn.renderEl(
      {el: '#okta-login-container'},
      function (res) {
        oktaSignIn.tokenManager.add('id_token', res[0]);
        oktaSignIn.tokenManager.add('access_token', res[1]);
        if (res.status === 'SUCCESS') {
            get_profile(oktaSignIn.tokenManager.get('access_token').accessToken);
        }
      },
      function error(err) {
        console.log('Unexpected error authenticating user: %o', err);
      }
    );
});
