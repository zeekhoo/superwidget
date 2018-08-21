var oktaSignIn = new OktaSignIn({
    baseUrl: 'https://[[org]]',
    clientId: '[[aud]]',
    redirectUri: '[[redirect]]',
    idpDiscovery: {
        requestContext: '/'
    },
    features: {
        idpDiscovery: true,
    },
});

oktaSignIn.session.get(function(res) {
    if (res.status==='ACTIVE') {
        window.location.href = '/login-noprompt?from=login_idp_disco';
    } else {
        oktaSignIn.renderEl(
            {el: '#okta-login-container'},
            function (res) {
                if (res.status === 'IDP_DISCOVERY') {
                    res.idpDiscovery.redirectToIdp('[[idp_disco]]');
                    return;
                } else {
                    window.location.href = '/login-noprompt?from=login_idp_disco';
                }
            }
        );
    }
});