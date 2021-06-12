var oktaSignIn = new OktaSignIn({ // Caution editing this section as you may break the demo.
    baseUrl: 'https://[[base_url]]',
    clientId: '[[aud]]',
    redirectUri: '[[redirect]]',
    authParams: {
        issuer: 'https://[[base_url]]/oauth2/[[iss]]',
        responseType: ['id_token','token'], //this app requires either 1) 'token+token' or 2) just 'code'
        scopes: [[scopes]],
        pkce: false // for implicit flows (responseType: id_token or token) set pkce=false
    },
    // Enable or disable widget functionality with the following options. Some of these features require additional configuration in your Okta admin settings. Detailed information can be found here: https://github.com/okta/okta-signin-widget#okta-sign-in-widget
    features: {
        router: true,                          // Leave this set to true for the API demo
        registration: false,                   // Enable self-service registration flow
        rememberMe: true,                      // Setting to false will remove the checkbox to save username
        //multiOptionalFactorEnroll: true,     // Allow users to enroll in multiple optional factors before finishing the authentication flow.
        //selfServiceUnlock: true,             // Will enable unlock in addition to forgotten password
        //smsRecovery: true,                   // Enable SMS-based account recovery
    	//callRecovery: true,                  // Enable voice call-based account recovery
    },
    // Look and feel changes
    logo: '[[base_icon]]',  // This demo includes other logos. Try: [logo_widgico.png, gear_logo.png, gear_half.png, okta32x32.png]
    language: 'en',         // Try: [fr, de, es, ja, zh-CN] Full list: https://github.com/okta/okta-signin-widget#language-and-text
    i18n: {
        //Overrides default text when using English. Override other languages by adding additional sections.
        'en': {
            'primaryauth.title': 'Sign In',    // Changes the sign in text
            'primaryauth.submit': 'Sign In',   // Changes the sign in button
            //'primaryauth.username.tooltip': 'Enter your APIDemo ID', // Changes the tooltip for username
            //'primaryauth.password.tooltip': 'Your APIDemo Password', // Changes the tooltip for password
            // More e.g. [primaryauth.username.placeholder,  primaryauth.password.placeholder, needhelp, etc.]. Full list here: https://github.com/okta/okta-signin-widget/blob/master/packages/@okta/i18n/src/properties/login.properties
        }
    }
});
oktaSignIn.renderEl( //Caution editing this section as you may break the demo.
    {el: '#okta-login-container'},
    function (res) {
        var key = '';
        if (res.tokens) {
            oktaSignIn.authClient.tokenManager.add('accessToken', res.tokens.accessToken);
            oktaSignIn.authClient.tokenManager.add('idToken', res.tokens.idToken);
            if (res.status === 'SUCCESS') {
                login(res.tokens.idToken, res.tokens.accessToken);
            }
        }
    }
);
