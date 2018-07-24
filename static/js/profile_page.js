var url = 'https://' + org;

Vue.filter('tostring', function (value) {
  if (!value)
    return '';
  else
    return value.toString().replace(/,/g, ", ");
});

Vue.filter('formatKey', function(value) {
    if (!value)
        return '';
    else
    {
        var words = value.split('_');
        var formatted = '';
        for (i in words) {
            formatted = formatted + words[i].charAt(0).toUpperCase() + words[i].slice(1) + ' ';
        }
        return formatted;
    }
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
        else if(this.accessToken && this.accessToken.groups && this.accessToken.groups.includes("Company Admin")){
          return "Company Administrator";
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
            profileApp.permissions = determinePermissions(profileApp.accessToken.groups, profileApp.accessToken.app_permissions);
            profileApp.accessTokenRaw = access_token;
            profileApp.accessTokenHeader = prettyPrint(window.atob(access_token_parts[0]));
            profileApp.accessTokenBody = prettyPrint(window.atob(access_token_parts[1]));
        }
      }
    });
}


//This function will look at group membership, and build a list of permissions
//that a user has based upon them.
function determinePermissions(groups, app_permissions) {
  if (!groups) {
    return '';
  }
  var perms = [];
  var desc = 'Can Report on ALL personnel,\r\n'  + app_permissions.join(',\r\n');
  groups.forEach(function(grp){
    if(grp == 'Admin') {
      perms.push({
        'Name': 'Administrator',
        'Criteria': 'Due to membership in the Admin group',
        'Desc': desc
      })
    }
    else if(grp == 'Company Admin') {
      perms.push({
        'Name': 'Company Administrator',
        'Criteria': 'Due to membership in the Company Admin group',
        'Desc': desc
      })
    }
  });
  if (perms.length == 0) {
      perms.push({
        'Name': 'User',
        'Criteria': 'Due to membership NOT in any Admin group',
        'Desc': desc
      });
  }

  return perms;
}

function showMyAppLinks(userId) {
    if (userId != null && userId != '') {
        $.ajax({
            url: url + "/api/v1/users/" + userId + "/appLinks",
            type: "GET",
            dataType: 'json',
            crossDomain: true,
            xhrFields: {
                withCredentials: true
            },
            statusCode: {
                200: function(res) {
                    if (res) {
                        document.getElementById("my_links").style.display = 'block';
                        profileApp.appLinks = res;
                    }
                }
            }
        });
    }
}
