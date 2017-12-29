//Note: "org", "iss" and "aud" variables were loaded outside this script
var base_url = 'https://' + org;            //e.g. 'https://zeekhoo.okta.com'
var issuer = base_url + '/oauth2/' + iss;   //e.g. 'https://zeekhoo.okta.com/oauth2/ausxkcyonq9Ht1uvi1t6'
var client_a = aud;                        //e.g. 'zXkxpyie6BCcutIWnk3B'

var client_b = '0oa4ox4jzjHj9vWgR1t7';
var client_id = client_a;
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
        'security.favorite_security_question': 'What was the super secret password OneAmerica mailed to you?',
        'password.forgot.emailSent.desc': 'Sent email to {0}. If you dont receive an email, please call (xxx)-yyy-zzzz',
        }
    }
});

oktaSignIn.on('pageRendered', function(data) {
    console.log('page=' + data.page);
    console.log('url=' + window.location);
    if(data.page==='mfa-verify'){
        console.log('bingo!');
//        oktaSignIn.hide();
    }
});

oktaSignIn.session.get(function (res) {
  console.log(res);

  if (res.status === 'ACTIVE') {
    get_profile(token);
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
