var base_url = 'https://' + org;

function showMyAppLinks(userId) {
    if (userId != null && userId != '') {
        url = base_url + "/api/v1/users/" + userId + "/appLinks";
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
                    profileapp.appLinks = linksJson;
                }
            }
        }
    }
}
