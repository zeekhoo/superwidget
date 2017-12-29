var baseUrl = 'https://' + org;            //e.g. 'https://zeekhoo.okta.com'
var issuer = baseUrl + '/oauth2/' + iss;   //e.g. 'https://zeekhoo.okta.com/oauth2/ausxkcyonq9Ht1uvi1t6'
var client_id = aud;                       //e.g. 'zXkxpyie6BCcutIWnk3B'
var redirect_uri = 'http://localhost:8000/oauth2/postback';
var idp_id = saml_idp;
var goo_id = goog;
var fb_id = fb;
var lnkd_id = lnkd;

var idps = [];
if (goo_id != 'None') {
    idps.push({type: 'GOOGLE', id: goo_id});
}
if (fb_id != 'None') {
    idps.push({type: 'FACEBOOK', id: fb_id});
}
if (lnkd_id != 'None') {
    idps.push({type: 'LINKEDIN', id: lnkd_id});
}

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
    baseUrl: baseUrl,
    clientId: client_id,
    redirectUri: redirect_uri,
    authParams: {
        issuer: issuer,
        display: 'popup',
        responseType: ['id_token', 'token'],
        scopes: [
            'openid', 'profile', 'email', 'address', 'phone',
            'com.zeek.p1.resource1.admin',
            'com.zeek.p1.resource1.user'
        ],
    },
    idps: idps,
    customButtons: btns,
    features: {
        rememberMe: true,
        autoPush: true,
        multiOptionalFactorEnroll: true,
        smsRecovery: true,
        callRecovery: false,
        selfServiceUnlock: true,
        router: true,
    }
});

oktaSignIn.session.get(function (res) {
  console.log(res);

  if (res.status === 'ACTIVE') {
    window.location.href='/tokens';
  }
  else {
    console.log('no session. render the login widget');
    oktaSignIn.renderEl(
      {el: '#okta-login-container'},
      function (res) {
        console.log(res);
        if (res[0]){
            oktaSignIn.tokenManager.add('id_token', res[0]);
            console.log('id_token=', res[0].idToken);
        }
        if (res[1]){
            oktaSignIn.tokenManager.add('access_token', res[1]);
            console.log('access_token=', res[1].accessToken);
        }
        if (res.status === 'SUCCESS') {
            console.log('success!');
            var token = oktaSignIn.tokenManager.get('access_token').accessToken;
            get_profile(token);
        }
      },
      function error(err) {
        console.log('Unexpected error authenticating user: %o', err);
      }
    );
  }
});
