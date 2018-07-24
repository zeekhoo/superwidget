
function listUsers(startsWith) {
    url = "/list-users";
    if (startsWith != null && startsWith != '') {
        url += '?startsWith=' + startsWith;
    }
    $.get(url, function(res) {
        if (res) {
            var resultsJson = JSON.parse(res);
            if (resultsJson) {
                document.getElementById("all_users").style.display = 'block';
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
                document.getElementById("all_users").style.display = 'none';
                getUserapp.allUser = resultsJson;
                document.getElementById("firstName_up").value= resultsJson.profile.firstName;
                document.getElementById("lastName_up").value= resultsJson.profile.lastName;
                document.getElementById("email_up").value= resultsJson.profile.email;
                document.getElementById("role_up").value= resultsJson.profile.customer_role;
                if (resultsJson.status == 'STAGED' || resultsJson.status == 'PROVISIONED') {
                    document.getElementById("resend_email").style.display = 'block';
                }
                document.getElementById("user_id_up").value= user_id;
                document.getElementById("companyName_up").value= resultsJson.profile.companyName;
                document.getElementById("vueapp-updateusers").style.display = 'block';
            }
        }
    });


}

function addUser(firstName, lastName, email, role, activate) {
    url = "/add-users?";
    if (firstName != null && firstName != '') {
        url += 'firstName=' + firstName;
    }
    if (lastName != null && lastName != '') {
        url += '&lastName=' + lastName;
    }
    if (email != null && email != '') {
        url += '&email=' + email;
    }
    if (role != null && role != '') {
        url += '&role=' + role;
    }
    if (activate != null && activate != '') {
        url += '&activate=' + activate;
    }
    $.get(url, function(res) {
        if (res) {
            var resultsJson = '';
        }
    });

}


function updateUser(firstName, lastName, email, role, companyName, user_id, deactivate, resend_email) {
    url = "/update-user?";
    if (firstName != null && firstName != '') {
        url += 'firstName=' + firstName;
    }
    if (lastName != null && lastName != '') {
        url += '&lastName=' + lastName;
    }
    if (email != null && email != '') {
        url += '&email=' + email;
    }
    if (role != null && role != '') {
        url += '&role=' + role;
    }
    if (deactivate != null && deactivate != '') {
        url += '&deactivate=' + deactivate;
    }
    if (resend_email != null && resend_email != '') {
        url += '&resend_email=' + resend_email;
    }
    if (user_id != null && user_id != '') {
        url += '&user_id=' + user_id;
    }
    if (companyName != null && companyName != '') {
        url += '&companyName=' + companyName;
    }
    $.get(url, function(res) {
        if (res) {
            var resultsJson = JSON.parse(res);
        }
    });

}
