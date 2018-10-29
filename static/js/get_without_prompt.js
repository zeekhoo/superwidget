function urlParams() {
    var urlParams;
    (window.onpopstate = function () {
        var match,
            pl     = /\+/g,  // Regex for replacing addition symbol with a space
            search = /([^&=]+)=?([^&]*)/g,
            decode = function (s) { return decodeURIComponent(s.replace(pl, " ")); },
            query  = window.location.search.substring(1);

        urlParams = {};
        while (match = search.exec(query))
           urlParams[decode(match[1])] = decode(match[2]);
    })();

    return urlParams;
}

var org = 'https://[[org]]';
//var params = urlParams();
//if (params['iss']) {
//    org = params['iss'];
//}

var options = {
    url: org,
    clientId: '[[aud]]',
    redirectUri: '[[redirect]]',
    issuer: org + '/oauth2/[[iss]]'
}

var authClient = new OktaAuth(options);

authClient.session.exists()
.then(function(exists) {
    if (exists) {
        authClient.token.getWithoutPrompt({
            responseType: ['id_token', 'token'],
            scopes: [[scopes]],
        })
        .then(function(tokens){
            showApp(tokens);
        })
        .then(function(err){
            console.log(err);
        })
    } else {
        console.log('not logged in');
    }
});

function showApp(res) {
    var key = '';
    if (res[0]) {
        key = Object.keys(res[0])[0];
        authClient.tokenManager.add(key, res[0]);
    }
    if (res[1]) {
        key = Object.keys(res[1])[0];
        authClient.tokenManager.add(key, res[1]);
    }
    post_tokens(authClient.tokenManager.get('idToken'), authClient.tokenManager.get('accessToken'));
}