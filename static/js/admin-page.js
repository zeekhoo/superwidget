function toggleComponents(component) {
    if (component != 'all_users')
        $('#all_users').hide();

    if (component != 'vueapp-addusers')
        $('#vueapp-addusers').hide();

    if (component != 'vueapp-updateusers')
        $('#vueapp-updateusers').hide();

    if (component != 'vueapp-addgroup')
        $('#vueapp-addgroup').hide();

    if (component != 'vueapp-groups')
        $('#vueapp-groups').hide();

    if (component != 'vueapp-perms')
        $('#vueapp-perms').hide();
}

function listUsers(startsWith) {
    toggleComponents('all_users');

    url = "/list-users";
    if (startsWith != null && startsWith != '') {
        url += '?startsWith=' + startsWith;
    }
    $.get(url, function(res) {
        if (res) {
            var resultsJson = JSON.parse(res);
            if (resultsJson) {
                $('#all_users').show();
                getUsersapp.allUsers = resultsJson;
            }
        }
    });
}

function listUser(user_id) {
    url = "/list-user";
    if (user_id != null && user_id != '') {
        url += '?user=' + user_id;
    }
    $.get(url, function(res) {
        if (res) {
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

    var accessToken = "";
    $.ajax({
        url: '/add-users',
        method: 'POST',
        data: data,
        contentType: 'application/x-www-form-urlencoded',
        crossDomain: true,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Authorization", "Bearer " + accessToken);
        },
        statusCode: {
            200: function(xhr) {
                console.log(xhr);
                var res = JSON.parse(xhr)
                console.log(res["status"]);
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

    var accessToken = "";
    $.ajax({
        url: '/update-user',
        method: 'POST',
        data: data,
        contentType: 'application/x-www-form-urlencoded',
        crossDomain: true,
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
    if (groupName != null && groupName != '') {
        url += '?groupName=' + groupName;
    }
    $.get(url, function(res) {
        if (res) {
            var resultsJson = '';
        }
    });
}

function listGroups() {
    toggleComponents('vueapp-groups');

    url = "/list-groups";
    $.get(url, function(res) {
        if (res) {
            var resultsJson = JSON.parse(res);
            if (resultsJson) {
                $("#vueapp-groups")[0].style.display='block';
                getGroupsapp.allGroups = resultsJson;
            }
        }
    });

}


function listPerms(group_id, group_name) {
    url = "/app-schema";
    $.get(url, function(res) {
        if (res) {
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
    url = "/list-perms";
    if (group_id != null && group_id != '') {
        url += '?group_id=' + group_id;
    }
    $.get(url, function(res) {
        if (res) {
            var resultsJson = JSON.parse(res);
            if (resultsJson) {
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

    url = "/update-perm";
    if (group_id != null && group_id != '') {
        url += '?group_id=' + group_id;
    }
    if (perms != null && perms != '') {
        url += '&perms=' + perms;
    }
    $.get(url, function(res) {
        if (res) {
            var resultsJson = JSON.parse(res);
        }
    });
}