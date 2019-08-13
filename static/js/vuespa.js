var id_token_str = srv_id_token || '';
var access_token_str = srv_access_token || '';
var url = 'https://' + org;

var navbarApp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vueapp-nav',
    data: {
        nameLabel: '',
        showAdminButton: false,
        showSensitiveButton: false,
        showDelegateButton: false,
        isAdmin: false,
        isCompanyAdmin: false
    }
})

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
        adminBadge: false,
        prfl: false,
        showDelegateButton: false,
        impersonationMode: false
    }
});

function usersGroups(accessToken, idToken) {
    if ("user_context" in (accessToken)) {
        if ("groups" in (accessToken.user_context)) {
            console.log(accessToken.user_context.groups);
            return accessToken.user_context.groups;
        }
    }
    if (app_permissions_claim in (accessToken)) {
        return accessToken[app_permissions_claim];
    }
    if (app_permissions_claim in (idToken)) {
        return idToken[app_permissions_claim];
    }
    return '';
}


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

var oktaSignIn = new OktaSignIn({
    baseUrl: url,
    clientId: aud,
    redirectUri: redirect_uri,
    authParams: {
        issuer: url + '/oauth2/' + iss
    }
});

function getFreshTokens() {
    oktaSignIn.session.get(function (res) {
        if (res.status === 'ACTIVE') {
            if (oktaSignIn.tokenManager.get('idToken')) {
                id_token_str = oktaSignIn.tokenManager.get('idToken').idToken;
            }
            if (oktaSignIn.tokenManager.get('accessToken')) {
                access_token_str = oktaSignIn.tokenManager.get('accessToken').accessToken;
            }
        }
    });
}

function showToken() {
    getFreshTokens();

    if (access_token_str != '') {
        var access_token_parts = access_token_str.split('.');
        profileApp.accessToken = JSON.parse(window.atob(access_token_parts[1]));
        profileApp.accessTokenRaw = access_token_str;
        profileApp.accessTokenHeader = prettyPrint(window.atob(access_token_parts[0]));
        profileApp.accessTokenBody = prettyPrint(window.atob(access_token_parts[1]));
    }
    if (id_token_str != '') {
        var id_token_parts = id_token_str.split('.');
        profileApp.idToken = JSON.parse(window.atob(id_token_parts[1]));
        profileApp.idTokenRaw = id_token_str;
        profileApp.idTokenHeader = prettyPrint(window.atob(id_token_parts[0]));
        profileApp.idTokenBody = prettyPrint(window.atob(id_token_parts[1]));
    }

    profileApp.prfl = profileOverride();
    navbarApp.nameLabel = profileApp.prfl.name;

    navbarApp.showDelegateButton = false; // Always init showDelegateButton = false
    var groupsList = appPermissions()
    if (groupsList.includes("companyadmin")) {
        navbarApp.showAdminButton=true;
        navbarApp.isCompanyAdmin=true;
    } else if (groupsList.includes("admin")){
        navbarApp.showAdminButton=true;
    }
    if (groupsList.includes("xfercash")) {
        navbarApp.showSensitiveButton=true;
    }

    if (profileApp.accessToken.user_context && profileApp.idToken.preferred_username != profileApp.accessToken.user_context.login)
        profileApp.impersonationMode = true;


    // After setting showAdminButton, we can set showDelegateButton
    if (!profileApp.impersonationMode) {
        if (profileApp.accessToken.scp.includes('groupadmin')) {
            navbarApp.showDelegateButton = true;
            profileApp.showDelegateButton = true;
        }
    }

    // Set admin badge and determine permissions after setting showDelegateButton
    profileApp.adminBadge = adminBadge();
    profileApp.permissions = determinePermissions();
}

function appPermissions() {
    var list = [];

    if (profileApp.showDelegateButton) {
        list = profileApp.prfl.groups;
    } else {
        var token = profileApp.prfl || profileApp.idToken;
        if (app_permissions_claim in (token))
            list = token[app_permissions_claim];
    }

    var result = new Array(list.length);
    for (var i=0; i < list.length; i++)
        result[i] = list[i].toLowerCase().replace(" ", "_").replace("_", "");

    return result;
}

function profileOverride() {
    if (profileApp.accessToken.user_context) {
        var usr_context = profileApp.accessToken.user_context;
        var delegated = {
            "given_name": usr_context.firstName,
            "family_name": usr_context.lastName,
            "name": usr_context.firstName + ' ' + usr_context.lastName,
            "preferred_username": usr_context.login,
            "email": usr_context.email || usr_context.login,
            "companyName": usr_context.companyName || profileApp.idToken.companyName,
            "groups": usersGroups(profileApp.accessToken, profileApp.idToken)
        };
        return delegated;
    }
    if (profile) {
        var p = JSON.parse(profile);
        return p;
    }
    return false;
}

function adminBadge() {
    if (profileApp.showDelegateButton) {
        return "Group Admin";
    }
    var list = appPermissions();
    if (list.includes("admin")) {
        return "Administrator";
    } else if (list.includes("companyadmin")) {
        return "Company Administrator";
    }
    return false;
}

//This function will look at group membership, and build a list of permissions
//that a user has based upon them.
function determinePermissions() {
    var perms = [];

    // Permissions based on groupadmin scope. This takes precedence
    if (profileApp.showDelegateButton) {
        perms.push({
            'Name': 'Group Admin',
            'Criteria': 'Due to having the "groupadmin" scope',
            'Desc': 'Can delegate users in groups: '
        })
    }

    // Permissions based on group membership
    if (perms.length == 0) {
        var app_permissions = appPermissions();
        app_permissions.forEach(function(perm){
            if(perm == 'admin') {
              perms.push({
                'Name': 'Administrator',
                'Criteria': 'Due to being assigned the Admin role',
                'Desc': 'Can lookup users.'
              })
            }
            else if(perm == 'companyadmin') {
              perms.push({
                'Name': 'Company Administrator',
                'Criteria': 'Due to being assigned the Company Admin role',
                'Desc': 'Can manage company resources.'
              })
            }
        });
    }

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
