function listGroups() {
    url = "/list-groups";
    $.get(url, function(res) {
        if (res) {
            var resultsJson = JSON.parse(res);
            if (resultsJson) {
                document.getElementById("all_groups").style.display = 'block';
                getGroupsapp.allGroups = resultsJson;

            }
        }
    });

}

function listPerms(group_id) {
    url = "/list-perms";
    if (group_id != null && group_id != '') {
        url += '?group_id=' + group_id;
    }
    $.get(url, function(res) {
        if (res) {
            var resultsJson = JSON.parse(res);
            if (resultsJson) {
                document.getElementById("all_perms").style.display = 'block';
                document.getElementById("group_id").value= group_id;
                getPermsapp.allPerms = resultsJson.profile.role_permissions;
                getGroup(group_id);
                updatePerms(group_id);
            }
        }
    });

}

function getGroup(group_id) {
    url = "/list-group";
    if (group_id != null && group_id != '') {
        url += '?group_id=' + group_id;
    }

    $.get(url, function(res) {
        if (res) {
            var resultsJson = JSON.parse(res);
            if (resultsJson) {
                document.getElementById("group_name").innerHTML = resultsJson.profile.name;

            }
        }
    });

}

function updatePerms(group_id) {
    url = "/list-perm";
    if (group_id != null && group_id != '') {
        url += '?group_id=' + group_id;
    }

    $.get(url, function(res) {
        if (res) {
            var resultsJson = JSON.parse(res);
            if (resultsJson) {
                var arrayLength = resultsJson.profile.role_permissions.length;
                for (var i = 0; i < arrayLength; i++) {
                    document.getElementById(resultsJson.profile.role_permissions[i]).checked = true;
                    document.getElementById("permList").value += resultsJson.profile.role_permissions[i] + ',';
                }
            }
        }
    });

}

function updatePermsGroup(group_id, perms) {
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
