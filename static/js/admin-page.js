$("#sw").keyup(function(event) {
    if (event.keyCode === 13) {
        $("#search-button").click();
    }
});


var authClient = new OktaAuth({url: 'https://{{ base_url }}'});
var accessToken = '';
if (srv_access_token != '') {
    //get the accessToken from session if it exists
    accessToken = srv_access_token;
} else if (authClient.tokenManager.get('accessToken')) {
    //get the accessToken stored in local storage
    accessToken = authClient.tokenManager.get('accessToken').accessToken;
}
showToken();

var adminButtonsApp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vueapp-adminbuttons',
    data: {
        isCompanyAdmin: navbarApp.isCompanyAdmin
    }
});

var getUsersapp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vueapp-users',
    data: {
        allUsers: [],
        isCompanyAdmin: navbarApp.isCompanyAdmin,
        showDelegateButton: navbarApp.showDelegateButton,
        orgAccessTokenString: false
    }
});

var addUserapp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vueapp-addusers',
    data: {
        firstName: '',
        lastName: '',
        email: '',
        role: '',
        companyName: '',
        activate: ''
    }
});

var updateUserApp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vueapp-updateusers',
    data: {
        isCompanyAdmin: navbarApp.isCompanyAdmin,
        userId: '',
        firstName: '',
        lastName: '',
        email: '',
        role: '',
        companyName: '',
        deactivate: '',
        resend_email: ''
    }
});

var getGroupsapp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vueapp-groups',
    data: {
        allGroups: []
    },
});

var addGroupApp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vueapp-addgroup',
    data: {
        groupName: ''
    }
});

var getPermsapp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vueapp-perms',
    data: {
        groupId: '',
        groupName: '',
        allPerms: '',
        perms: ''
    },
});

var idToken = '';
if (srv_id_token != '') {
    //get the idToken from session if it exists
    idToken = srv_id_token;
} else if (authClient.tokenManager.get('idToken')) {
    //get the idToken stored in local storage
    idToken = authClient.tokenManager.get('idToken').idToken;
}

function listUsers(startsWith) {
    toggleComponents('all_users');

    var bearerToken = accessToken;
    if (getUsersapp.orgAccessTokenString)
        bearerToken = getUsersapp.orgAccessTokenString;

    data = {};
    if (startsWith != null && startsWith != '') {
        data.startsWith = startsWith;
    }
    $.ajax({
        url: '/list-users',
        method: 'GET',
        data: data,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Authorization", "Bearer " + bearerToken);
        },
        success: function(res) {
            var resultsJson = JSON.parse(res);
            if (resultsJson) {
                $('#all_users').show();
                getUsersapp.allUsers = resultsJson;
            }
        }
    });
}

function listUser(user_id) {
    data = {}
    if (user_id != null && user_id != '') {
        data.user = user_id;
    }
    $.ajax({
        url: '/list-user',
        method: 'GET',
        data: data,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Authorization", "Bearer " + accessToken);
        },
        success: function(res) {
            var resultsJson = JSON.parse(res);
            if (resultsJson) {
                $("#vueapp-updateusers").show();
                $("#all_users").hide();

                updateUserApp.firstName = resultsJson.profile.firstName;
                updateUserApp.lastName = resultsJson.profile.lastName;
                updateUserApp.email = resultsJson.profile.email;
                updateUserApp.role = resultsJson.profile.customer_role;
                updateUserApp.companyName = resultsJson.profile.companyName;
                updateUserApp.userId = user_id;
                if (resultsJson.status == 'STAGED' || resultsJson.status == 'PROVISIONED')
                    $("#resend_email").show();
            }
        }
    });
}

function addUser() {
    data = {};
    if (addUserapp.firstName != null && addUserapp.firstName != '')
        data.firstName = addUserapp.firstName;
    if (addUserapp.lastName != null && addUserapp.lastName != '')
        data.lastName = addUserapp.lastName;
    if (addUserapp.email != null && addUserapp.email != '')
        data.email = addUserapp.email;
    if (addUserapp.role != null && addUserapp.role != '')
        data.role = addUserapp.role;
    if (addUserapp.activate != null && addUserapp.activate != '')
        data.activate = addUserapp.activate;

    $.ajax({
        url: '/add-users',
        method: 'POST',
        data: data,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Authorization", "Bearer " + accessToken);
        },
        statusCode: {
            200: function(xhr) {
                var res = JSON.parse(xhr);
                if ("id" in res) {
                    $('#sw').val(addUserapp.email);

                    addUserapp.firstName = '';
                    addUserapp.lastName = '';
                    addUserapp.email = '';
                    addUserapp.role = '';
                    addUserapp.activate = '';

                    listUsers($('#sw').val());
                } else {
                    console.log(res);
                }
            }
        }
    });
}


function updateUser() {
    data = {};
    if (updateUserApp.userId != null && updateUserApp.userId != '')
        data.user_id=updateUserApp.userId;
    if (updateUserApp.firstName != null && updateUserApp.firstName != '')
        data.firstName = updateUserApp.firstName;
    if (updateUserApp.lastName != null && updateUserApp.lastName != '')
        data.lastName=updateUserApp.lastName;
    if (updateUserApp.email != null && updateUserApp.email != '')
        data.email=updateUserApp.email;
    if (updateUserApp.role != null && updateUserApp.role != '')
        data.role=updateUserApp.role;
    if (updateUserApp.deactivate != null && updateUserApp.deactivate != '')
        data.deactivate=updateUserApp.deactivate;
    if (updateUserApp.resend_email != null && updateUserApp.resend_email != '')
        data.resend_email=updateUserApp.resend_email;
    if (updateUserApp.companyName != null && updateUserApp.companyName != '')
        data.companyName=updateUserApp.companyName;

    $.ajax({
        url: '/update-user',
        method: 'POST',
        data: data,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Authorization", "Bearer " + accessToken);
        },
        statusCode: {
            200: function(xhr) {
                var res = JSON.parse(xhr)
                if (res["status"] && res["status"] === 'PROVISIONED' || 'STAGED' || 'ACTIVE') {
                    var searchedUsers = getUsersapp.allUsers;
                    for (i in searchedUsers) {
                        var row = searchedUsers[i];
                        if (row.id === data.user_id) {
                            if ('email' in data) {
                                row.profile.login = data.email;
                                row.profile.email = data.email;
                            }
                            if ('firstName' in data)
                                row.profile.firstName = data.firstName;
                            if ('lastName' in data)
                                row.profile.lastName = data.lastName;
                            if ('role' in data)
                                row.profile.customer_role = data.role;
                        }
                    }

                    $('#vueapp-updateusers').hide();
                    $('#all_users').show();
                } else {
                    console.log(xhr);
                }
            }
        }
    });
}

function addGroup(groupName) {
    url = "/add-group";
    data = {};
    if (addGroupApp.groupName != null && addGroupApp.groupName != '') {
        data.groupName = addGroupApp.groupName;

        $.ajax({
            url: '/add-group',
            method: 'POST',
            data: data,
            beforeSend: function (xhr) {
                xhr.setRequestHeader("Authorization", "Bearer " + accessToken);
            },
            statusCode: {
                200: function(xhr) {
                    var res = JSON.parse(xhr);
                    if ("id" in res) {
                        addGroupApp.groupName = '';
                        listGroups();
                    }
                    else {
                        console.log(res);
                    }
                }
            }
        });
    }
}

function listGroups() {
    toggleComponents('vueapp-groups');

    $.ajax({
        url: '/list-groups',
        method: 'GET',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Authorization", "Bearer " + accessToken);
        },
        success: function(res) {
            var resultsJson = JSON.parse(res);
            if (resultsJson) {
                $("#vueapp-groups")[0].style.display='block';
                getGroupsapp.allGroups = resultsJson;
            }
        }
    });
}


function listPerms(group_id, group_name) {
    $.ajax({
        url: '/app-schema',
        method: 'GET',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Authorization", "Bearer " + accessToken);
        },
        success: function(res) {
            var resultsJson = JSON.parse(res);
            if (resultsJson) {
                $('#vueapp-perms')[0].style.display='block';

                var data = [];
                var role_permissions = resultsJson.definitions.custom.properties.role_permissions.items.enum;
                for (i in role_permissions) {
                    var grp_name = '';
                    if (i == 0) {
                        grp_name = group_name;
                    }
                    var perm = {
                        value: role_permissions[i],
                        selected: false,
                        groupName: grp_name
                    };
                    data.push(perm);
                }
                getPermsapp.allPerms = data;
                getPermsapp.groupName = group_name;
                getPermsapp.groupId = group_id;

                selectedPerms(group_id, group_name);
            }
        }
    });
}

function selectedPerms(group_id, group_name) {
    data = {};
    if (group_id != null && group_id != '') {
        data.group_id = group_id;
    }

    $.ajax({
        url: '/list-perms',
        method: 'GET',
        data: data,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Authorization", "Bearer " + accessToken);
        },
        success: function(res) {
            var resultsJson = JSON.parse(res);
            if (resultsJson.profile) {
                var allPerms = getPermsapp.allPerms;
                var role_permissions = resultsJson.profile.role_permissions;
                for (i in role_permissions) {
                    var perm = role_permissions[i];
                    for (j in allPerms) {
                        if (allPerms[j].value === role_permissions[i]){
                            allPerms[j].selected = true;
                        }
                    }
                }
            }
        }
    });
}


function selectPerm(selected, checked) {
    var perms = getPermsapp.allPerms;
    for (i in perms) {
        var perm = perms[i];
        if (perm.value === selected) {
            perm.selected = checked;
        }
    }
}

function updatePermsGroup() {
    var group_id = getPermsapp.groupId;
    var allPerms = getPermsapp.allPerms;
    var perms = "";
    for (i in allPerms) {
        var perm = allPerms[i];
        if (perm.selected === true) {
            perms += perm.value + ',';
        }
    }

    data = {};
    if (group_id != null && group_id != '') {
        data.group_id = group_id;
    }
    if (perms != null && perms != '') {
        data.perms = perms;
    }

    $.ajax({
        url: '/update-perm',
        method: 'POST',
        data: data,
        contentType: 'application/x-www-form-urlencoded',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Authorization", "Bearer " + accessToken);
        },
        complete: function(res, xhr, settings) {
            console.log(res);
        }
    });
}

function doProxyLogin(target) {
    data = {
        "delegation_target": target
    }
    $.ajax({
        url: delegation_service_endpoint + '/delegate/init',
        method: 'POST',
        data: JSON.stringify(data),
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.setRequestHeader("Authorization", "Bearer " + accessToken);
        },
        complete: function(res, xhr, settings) {
            console.log(JSON.stringify(res));
            if (res.responseJSON.status === 'SUCCESS') {
                window.location = '/login-noprompt';
            }
        }
    });
}


function proxyLogin(target) {
    data = {
        "delegation_target": target
    }
    $.ajax({
        url: '/delegate-init',
        method: 'POST',
        data: JSON.stringify(data),
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.setRequestHeader("Authorization", "Bearer " + accessToken);
        },
        complete: function(res, xhr, settings) {
            console.log(JSON.stringify(res));
            if (res.responseJSON.status === 'SUCCESS') {
                window.location = '/login-noprompt';
            }
        }
    });
}


function toggleComponents(component) {
    if (component === 'all_users')
        $('#all_users').show();
    else
        $('#all_users').hide();

    if (component === 'vueapp-addusers')
        $('#vueapp-addusers').show();
    else
        $('#vueapp-addusers').hide();

    if (component === 'vueapp-updateusers')
        $('#vueapp-updateusers').show();
    else
        $('#vueapp-updateusers').hide();

    if (component === 'vueapp-addgroup')
        $('#vueapp-addgroup').show();
    else
        $('#vueapp-addgroup').hide();

    if (component === 'vueapp-groups')
        $('#vueapp-groups').show();
    else
        $('#vueapp-groups').hide();

    if (component === 'vueapp-perms')
        $('#vueapp-perms').show();
    else
        $('#vueapp-perms').hide();
}


function getAccessTokenFragment(param) {
    if (param) {
        var access_token = param.split("&")[0].split("#")[1].split('=')[1];
        if (access_token) {
            return access_token;
        }
    }
    return false;
}
getUsersapp.orgAccessTokenString = getAccessTokenFragment(window.location.hash);