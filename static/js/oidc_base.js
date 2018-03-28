var oktaSignIn = new OktaSignIn({ //Do not edit this section.
    baseUrl: 'https://[[org]]',
    clientId: '[[aud]]',
    redirectUri: '[[redirect]]',
    authParams: {
        issuer: 'https://[[org]]/oauth2/[[iss]]',
        responseType: ['id_token', 'token'],
        scopes: [[scopes]],
    },
    features: {
    //These affect the functionality of the widget and will enable or disable capabilities
    //Detailed feature information can be found here: https://github.com/okta/okta-signin-widget#okta-sign-in-widget 
        router: true, //Leave this set to true for the API demo
        registration: false, //Enable self-service registration flow
        rememberMe: true, //Setting to false will remove the checkbox to save username
        //multiOptionalFactorEnroll: true, //Allow users to enroll in multiple optional factors before finishing the authentication flow. 
        //selfServiceUnlock: true, //Will enable unlock in addition to forgotten password
        //smsRecovery: true, //Enable SMS-based account recovery
    	//callRecovery: true, //Enable voice call-based account recovery
    },
    // Look and feel changes
    logo: '/static/img/gear_half.png', //Other included logos: logo_widgico.png, gear_logo.png, gear_half.png
    language: 'en', //Suggested languages include fr, de, es 
    i18n: {
    //Customizes the text for the widget when using English. Additional sections can be added to customize other languages. 
        'en': {
            'primaryauth.title': 'Sign In', //Changes the sign in text
            'primaryauth.submit': 'Sign In', //Changes the sign in button
            //'primaryauth.username.tooltip': 'Enter your APIDemo ID', //Changes the tooltip for username
            //'primaryauth.password.tooltip': 'Your APIDemo Password', //Changes the tooltip for password
            //Example more tags: [primaryauth.username.placeholder,  primaryauth.password.placeholder, needhelp, etc.]
            //Full list here: https://github.com/okta/okta-signin-widget/blob/master/packages/@okta/i18n/dist/properties/login.properties
        }
    },
});
oktaSignIn.renderEl( //Do not edit this section.
    {el: '#okta-login-container'},
    function (res) {
        var key = '';
        if (res[0]) {
            key = Object.keys(res[0])[0];
            oktaSignIn.tokenManager.add(key, res[0]);
        }
        if (res[1]) {
            key = Object.keys(res[1])[0];
            oktaSignIn.tokenManager.add(key, res[1]);
        }
        if (res.status === 'SUCCESS') {
            get_profile(key, oktaSignIn.tokenManager.get(key));
        }
    }
);

