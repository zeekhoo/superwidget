function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            console.log('cookie' + i + ': ' + cookie);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function prettyPrint(ugly) {
    var obj = JSON.parse(ugly);
    return JSON.stringify(obj, undefined, 4);
}

function get_profile(access_token) {

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/oauth2/postback');
    //xhr.setRequestHeader('X-CSRFToken', csrftoken); /*too lazy...used csrf_exempt*/

    var formData = new FormData();
    formData.append("access_token", access_token);
    xhr.send(formData);

    xhr.onreadystatechange = function() {
        window.location.href = '/profile';
    }
}

function openInNewTab(url) {
  var win = window.open(url, '_blank');
  win.focus();
}

function link_to_widget_js() {
    var codeHref = document.getElementById('code-href');
    if (codeHref) {
        if (codeHref.innerHTML == 'Hide widget code...') {
            codeHref.innerHTML = 'Show widget code...';

            var codePreview = document.getElementById('code-preview');
            if (codePreview) {
                codePreview.style.display = 'none';
            }
            return;
        }
    }


    var js_location = '/static/js/oidc_css.js';

    var profilePage = profile_page.split('/')[1];
    var tokensPage = tokens_page.split('/')[1];
    var delAuth = del_auth_url.split('/')[1];
    var hostedPage = hosted_login_url.split('/')[1];
    var customPage = authjs_page.split('/')[1];

    var pathArray = window.location.pathname.split('/');
    if (pathArray[1]) {
        if (pathArray[1] === delAuth) {
            js_location = '/static/js/oidc_idp.js'
        } else if (pathArray[1] === hostedPage) {
            js_location = '/static/js/default-okta-signin-pg.js'
        } else if (pathArray[1] === customPage) {
            js_location = '/static/js/custom_ui.js'
        }
        console.log('profile page: ' + profilePage);
        console.log('tokens page: ' + tokensPage);
        console.log('page = ' + pathArray[1]);
        if (pathArray[1] === profilePage || pathArray[1] === tokensPage) {
            openInNewTab(js_location);
            return;
        }
    }
    getJs(js_location, 'js-area');
}


function getJs(location, target) {
    var url = location;
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", url, true);
    xhttp.send();
    xhttp.onreadystatechange = function() {
        var area = document.getElementById(target);
        if (area) {
            area.innerHTML = xhttp.responseText;

            var codePreview = document.getElementById('code-preview');
            if (codePreview) {
                codePreview.style.display = 'block';

                var codeHref = document.getElementById('code-href');
                if (codeHref) {
                    codeHref.innerHTML = 'Hide widget code...';
                }
            }
        }
    }
}
