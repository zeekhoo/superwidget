var id_token_str = srv_id_token;
var access_token = srv_access_token;
var url = 'https://' + org;
var oktaSignIn = new OktaSignIn({
    baseUrl: url,
    clientId: aud,
    redirectUri: redirect_uri,
    authParams: {
        issuer: url + '/oauth2/' + iss
    }
});


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

var navApp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vueapp-nav',
    computed: {
        nameLabel: function() {
            if (profile) {
                var prfl = JSON.parse(profile);
                return prfl.name;
            }
            return '';
        },
        showAdminButton: function() {
            var list = appPermissions();
            if (list.includes("admin") || list.includes("company_admin")) {
                return true;
            }
            return false;
        }
    }
});

var profileApp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vueapp-profile',
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
        permissions: false,
    },
    computed: {
        prfl: function() {
            if (profile) {
                var prfl = JSON.parse(profile);
                return prfl;
            }
            return false;
        },
        adminBadge: function () {
            if(this.idToken){
                var list = appPermissions();
                if (list.includes("admin")) {
                    return "Administrator";
                } else if (list.includes("company_admin")) {
                    return "Company Administrator";
                }
            }
            return false;
        },
        isAdmin: function() {
            var str = this.adminBadge;
            if (str && str.includes('Administrator')) {
                return true;
            }
            return false;
        },
        isCompanyAdmin: function() {
            var str = this.adminBadge;
            if (str && str.includes('Administrator') && str.includes('Company')) {
                return true;
            }
            return false;
        }
    }
});

function appPermissions() {
    var list = [];

    oktaSignIn.session.get(function (res) {
        console.log(res);
        if (res.status === 'ACTIVE') {
            if (oktaSignIn.tokenManager.get('idToken')) {
                id_token_str = oktaSignIn.tokenManager.get('idToken').idToken;
            }
        }
    });
    if (id_token_str != '') {
        var decodedIdToken = JSON.parse(window.atob(id_token_str.split('.')[1]));
        if (app_permissions_claim in decodedIdToken) {
            list = decodedIdToken[app_permissions_claim];
            console.log('list ' + app_permissions_claim + ':' + list);
        }
        for (var i=0; i < list.length; i++) {
            list[i] = list[i].toLowerCase().replace(" ", "_");
        }
    }
    return list;
}

function showToken() {
    oktaSignIn.session.get(function (res) {
        console.log(res);
        if (res.status === 'ACTIVE') {
            if (oktaSignIn.tokenManager.get('idToken')) {
                id_token_str = oktaSignIn.tokenManager.get('idToken').idToken;
            }
            if (oktaSignIn.tokenManager.get('accessToken')) {
                access_token = oktaSignIn.tokenManager.get('accessToken').accessToken;
            }
        }
    });

    if (id_token_str != '') {
        var id_token_parts = id_token_str.split('.');
        profileApp.idToken = JSON.parse(window.atob(id_token_parts[1]));
        profileApp.idTokenRaw = id_token_str;
        profileApp.idTokenHeader = prettyPrint(window.atob(id_token_parts[0]));
        profileApp.idTokenBody = prettyPrint(window.atob(id_token_parts[1]));
    }
    if (access_token != '') {
        var access_token_parts = access_token.split('.');
        profileApp.accessToken = JSON.parse(window.atob(access_token_parts[1]));
        profileApp.permissions = determinePermissions();
        profileApp.accessTokenRaw = access_token;
        profileApp.accessTokenHeader = prettyPrint(window.atob(access_token_parts[0]));
        profileApp.accessTokenBody = prettyPrint(window.atob(access_token_parts[1]));
    }
}


//This function will look at group membership, and build a list of permissions
//that a user has based upon them.
function determinePermissions() {
    var perms = [];

    var app_permissions = appPermissions();

    var desc = ''
    if (app_permissions) {
      desc += ', ' + app_permissions.join(',\r\n');
    }

    app_permissions.forEach(function(perm){
    if(perm == 'admin') {
      perms.push({
        'Name': 'Administrator',
        'Criteria': 'Due to being assigned the Admin role in Okta.',
        'Desc': 'Can lookup users.'
      })
    }
    else if(perm == 'company_admin') {
      perms.push({
        'Name': 'Company Administrator',
        'Criteria': 'Due to being assigned the Company Admin role in Okta.',
        'Desc': 'Can manage company resources.'
      })
    }
    });
    if (perms.length == 0) {
      var userPermissions = 'No Privileged Permissions';
      perms.push({
        'Name': 'User',
        'Criteria': 'Due to membership NOT in any Admin group',
        'Desc': userPermissions
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
