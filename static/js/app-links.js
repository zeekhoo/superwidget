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
                    var apps = new Vue({
                        delimiters: ['[[', ']]'],
                        el: '#vueapp',
                        data: {
                            appLinks: linksJson
                        }
                    });
                    //drawTable(linksJson);
                }
            }
        }
    }
}

function drawTable(tableData) {
    var i;
    var draw = "";
    for(i = 0; i < tableData.length; i++) {
        draw += '<tr><td>' +
        '<a href="' + tableData[i].linkUrl + '" target="_blank">' +
        '<img src="' + tableData[i].logoUrl + '" class="img-rounded">' +
        '<label>&nbsp;&nbsp;' + tableData[i].label + '</label>' +
        '</a>' +
        '</td></tr>';
    }
    document.getElementById("my_links").innerHTML = draw;
}
