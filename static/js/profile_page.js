var url = 'https://' + org;

Vue.filter('tostring', function (value) {
  if (!value)
    return '';
  else
    return value.toString().replace(/,/g, ", ");
});

var data = [];
var profileApp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vueapp',
    data: {
        idToken: false,
        idTokenRaw: false,
        idTokenHeader: false,
        idTokenBody: false,
        accessToken: false,
        accessTokenRaw: false,
        accessTokenBody: false,
        accessTokenHeader: false,
        appLinks: false,
        prfl: JSON.parse(profile),
        permissions: false,
    },
    computed: {
      adminBadge: function () {
        if(this.accessToken && this.accessToken.groups && this.accessToken.groups.includes("Admin")) {
          return "Administrator";
        }
        else if(this.accessToken && this.accessToken.groups && this.accessToken.groups.includes("Department Admin")){
          return "Departmental Administrator";
        }
        else {
          return false;
        }
      }
    }
});


function showToken(org, aud, iss, uri) {
    var oktaSignIn = new OktaSignIn({
        baseUrl: url,
        clientId: aud,
        redirectUri: uri,
        authParams: {
            issuer: url + '/oauth2/' + iss
        }
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
}


//This function will look at group membership, and build a list of permissions
//that a user has based upon them.
function determinePermissions(groups) {
  if (!groups) {
    return '';
  }
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

function showMyAppLinks(userId) {
    if (userId != null && userId != '') {
        url = url + "/api/v1/users/" + userId + "/appLinks";
        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", url, true);
        xhttp.withCredentials = true;
        xhttp.send();
        xhttp.onreadystatechange = function() {
            var res = xhttp.responseText;
            if (res) {
                var linksJson = JSON.parse(res);
                if (linksJson) {
                    document.getElementById("my_links").style.display = 'block';
                    profileApp.appLinks = linksJson;
                }
            }
        }
    }
}
