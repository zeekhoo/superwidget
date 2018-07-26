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
                getUserapp.allUser = resultsJson;

                updateUserapp.firstName = resultsJson.profile.firstName;
                updateUserapp.lastName = resultsJson.profile.lastName;
                updateUserapp.email = resultsJson.profile.email;
                updateUserapp.role = resultsJson.profile.customer_role;
                updateUserapp.companyName = resultsJson.profile.companyName;
                updateUserapp.userId = user_id;
                if (resultsJson.status == 'STAGED' || resultsJson.status == 'PROVISIONED')
                    $("#resend_email").show();

//                $("#firstName_up").val(resultsJson.profile.firstName);
//                $("#lastName_up").val(resultsJson.profile.lastName);
//                $("#email_up").val(resultsJson.profile.email);
//                $("#role_up").val(resultsJson.profile.customer_role);
//                $("#user_id_up").val(user_id);
//                $("#companyName_up").val(resultsJson.profile.companyName);
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
    if (updateUserapp.userId != null && updateUserapp.userId != '')
        data.user_id=updateUserapp.userId;
    if (updateUserapp.firstName != null && updateUserapp.firstName != '')
        data.firstName = updateUserapp.firstName;
    if (updateUserapp.lastName != null && updateUserapp.lastName != '')
        data.lastName=updateUserapp.lastName;
    if (updateUserapp.email != null && updateUserapp.email != '')
        data.email=updateUserapp.email;
    if (updateUserapp.role != null && updateUserapp.role != '')
        data.role=updateUserapp.role;
    if (updateUserapp.deactivate != null && updateUserapp.deactivate != '')
        data.deactivate=updateUserapp.deactivate;
    if (updateUserapp.resend_email != null && updateUserapp.resend_email != '')
        data.resend_email=updateUserapp.resend_email;
    if (updateUserapp.companyName != null && updateUserapp.companyName != '')
        data.companyName=updateUserapp.companyName;

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
                console.log(xhr);
                var res = JSON.parse(xhr)
                console.log(res["status"]);
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