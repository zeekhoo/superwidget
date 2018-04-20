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

