//must initialize "org", "iss", "aud" and "raas_flag" variables outside this script
var base_url = 'https://' + org;            //e.g. 'https://zeekhoo.okta.com'
var issuer = base_url + '/oauth2/' + iss;   //e.g. 'https://zeekhoo.okta.com/oauth2/ausxkcyonq9Ht1uvi1t6'
var client_id = aud;                        //e.g. 'zXkxpyie6BCcutIWnk3B'
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
            'openid', 'profile', 'email', 'address', 'phone',
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
		registration: raas_flag
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
  console.log('token = ' + token);

  if (res.status === 'ACTIVE' && token) {
    get_profile(token.access_token);
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
            console.log('access_token=', oktaSignIn.tokenManager.get('access_token').accessToken);
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
