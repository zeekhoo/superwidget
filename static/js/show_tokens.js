function showToken(org, aud, iss, uri) {
    var baseUrl = 'https://' + org;
    var issuer = baseUrl + '/oauth2/' + iss;

    var oktaSignIn = new OktaSignIn({
        baseUrl: baseUrl,
        clientId: aud,
        redirectUri: uri,
        authParams: {
            issuer: issuer
        }
    });

    oktaSignIn.session.get(function (res) {
      console.log(res);
      if (res.status === 'ACTIVE') {
        console.log('have session');
        console.log('user_id = ' + res.userId);

        if (oktaSignIn.tokenManager.get('idToken')) {
            populateFields('id_token', oktaSignIn.tokenManager.get('idToken').idToken);
        } else {
            populateFields('id_token', srv_id_token);
        }
        if (oktaSignIn.tokenManager.get('accessToken')) {
            populateFields('access_token', oktaSignIn.tokenManager.get('accessToken').accessToken);
        } else {
            populateFields('access_token', srv_access_token);
        }
      }
    });
}


function populateFields(elementId, token) {
    var token_parts = token.split('.');
    document.getElementById(elementId).innerHTML = token;
    document.getElementById(elementId + '_header').innerHTML = prettyPrint(window.atob(token_parts[0]));
    document.getElementById(elementId + '_decoded').innerHTML = prettyPrint(window.atob(token_parts[1]));
}

function prettyPrint(ugly) {
    var obj = JSON.parse(ugly);
    return JSON.stringify(obj, undefined, 4);
}




