var authClient = new OktaAuth({url: 'https://[[impersonation_org]]'});

var hash = window.location.hash.substr(1);
var result = hash.split('&');
for (var i=0; i < result.length; i++) {
    var param = result[i].split('=');
    console.log(param[0] + ': ' + param[1]);
    if (param[0] == 'id_token') {
        var idToken = {idToken: param[1], scopes: [], expiresAt: 123};
        authClient.tokenManager.add('idToken', idToken);
    }
    if (param[0] == 'access_token') {
        var accessToken = {accessToken: param[1], scopes: [], expiresAt: 123};
        authClient.tokenManager.add('accessToken', accessToken);
    }
}

//destroy session
authClient.signOut();

//show the app
get_profile('accessToken', authClient.tokenManager.get('accessToken'));
