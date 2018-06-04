var url = 'https://' + org;

var oktaSignIn = new OktaSignIn({
    baseUrl: url
});

oktaSignIn.session.get(function (res) {
  console.log(res);
  if (res.status === 'ACTIVE') {
    console.log('have session');
    console.log('user_id = ' + res.userId);
    var id_token = srv_id_token;
    if (oktaSignIn.tokenManager.get('idToken')) {
        id_token = oktaSignIn.tokenManager.get('idToken').idToken;
    }
    var access_token = srv_access_token;
    if (oktaSignIn.tokenManager.get('accessToken')) {
        var access_token = oktaSignIn.tokenManager.get('accessToken').accessToken;
    }
    if (id_token != '') {
        var id_token_parts = id_token.split('.');
        profileApp.idToken = JSON.parse(window.atob(id_token_parts[1]));
        profileApp.idTokenRaw = id_token;
        profileApp.idTokenHeader = prettyPrint(window.atob(id_token_parts[0]));
        profileApp.idTokenBody = prettyPrint(window.atob(id_token_parts[1]));
    }
    if (access_token != '') {
        var access_token_parts = access_token.split('.');
        profileApp.accessToken = JSON.parse(window.atob(access_token_parts[1]));
        profileApp.permissions = determinePermissions(profileApp.accessToken.groups);
        profileApp.accessTokenRaw = access_token;
        profileApp.accessTokenHeader = prettyPrint(window.atob(access_token_parts[0]));
        profileApp.accessTokenBody = prettyPrint(window.atob(access_token_parts[1]));
    }
  }
});

/*
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
*/

//This function will look at group membership, and build a list of permissions
//that a user has based upon them.
function determinePermissions(groups) {
  var perms = [];
  groups.forEach(function(grp){
    if(grp == 'Admin') {
      perms.push({
        'Name': 'Administrator',
        'Criteria': 'Due to membership in the Admin group',
        'Desc': 'Can Report on ALL personnel'
      })
    }
    else if(grp == 'Department Admin') {
      perms.push({
        'Name': 'Administrator',
        'Criteria': 'Due to membership in the Department Admin group',
        'Desc': 'Can report on active personnel in the same department'
      })
    }
  });
  return perms;
}