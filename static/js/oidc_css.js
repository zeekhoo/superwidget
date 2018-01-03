//must initialize "org", "iss", "aud" and "raas_flag" variables outside this script
var base_url = 'https://' + org;            //e.g. 'https://login.alwaysaasure.com';
var issuer = base_url + '/oauth2/' + iss;   //e.g. 'https://login.alwaysaasure.com/oauth2/default';
var client_id = aud;                        //e.g. '0oadbg08aaYtrMlRC0h7';
var showSelfServiceReg = raas_flag;         //e.g. false;
var redirect_uri = 'http://localhost:8000/oauth2/postback';


var oktaSignIn = new OktaSignIn({
    baseUrl: base_url,
    clientId: client_id,
    redirectUri: redirect_uri,
    language: 'en',
    logo: '',
    authParams: {
        issuer: issuer,
        responseType: ['id_token', 'token'],
        scopes: [
            'openid', 'profile', 'email', 'address', 'phone', 'offline_access',
            'com.zeek.p1.resource1.admin',
            'com.zeek.p1.resource1.user'
        ],
    },
    features: {
        rememberMe: true,
        autoPush: true,
        multiOptionalFactorEnroll: true,
        smsRecovery: true,
        callRecovery: false,
        selfServiceUnlock: true,
        router: true,
		registration: showSelfServiceReg
    },
    i18n: {
        'en': {
            'primaryauth.submit': 'Login',
            'needhelp': 'Need help?',
            'password.forgot.email.or.username.placeholder': 'Username',
        }
    }
});

oktaSignIn.session.get(function (res) {
  console.log(res);

  var token = oktaSignIn.tokenManager.get('access_token');
  if (res.status === 'ACTIVE' && token) {
    get_profile(token.accessToken);
  }
  else {
    console.log('no session. render the login widget');
    oktaSignIn.renderEl(
      {el: '#okta-login-container'},
      function (res) {
        if (res[0]){
            console.log('id_token=', res[0].idToken);
            oktaSignIn.tokenManager.add('id_token', res[0]);
        }
        if (res[1]){
            console.log('access_token=', res[1].accessToken);
            oktaSignIn.tokenManager.add('access_token', res[1]);
        }
        if (res.status === 'SUCCESS') {
            console.log('success!');
            token = oktaSignIn.tokenManager.get('access_token');
            get_profile(token.accessToken);
        }
      },
      function error(err) {
        console.log('Unexpected error authenticating user: %o', err);
      }
    );
  }
});
