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

function get_profile(token_type, token) {

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/oauth2/callback');
    //xhr.setRequestHeader('X-CSRFToken', csrftoken); /*too lazy...used csrf_exempt*/

    var formData = new FormData();
    if (token_type === 'accessToken')
        formData.append('access_token', token.accessToken);
    else
        formData.append('id_token', token.idToken);
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
        if (pathArray[1] === profilePage || pathArray[1] === tokensPage) {
            openInNewTab(js_location);
            return;
        }
    }
}


function toggleJsView(buttonId) {
    var showOrHide = document.getElementById(buttonId);
    var area = document.getElementById('code-preview');
    var bs3 = document.getElementById('widget-b3');

    if (showOrHide && area) {
        if (showOrHide.innerHTML.indexOf('Show') != '-1') {
            area.style.display = 'block';
            showOrHide.innerHTML = showOrHide.innerHTML.replace('Show', 'Hide');
            if (bs3) {
                bs3.setAttribute('class', 'col-md-4');
            }
            var myCode = document.getElementById("theScript").innerHTML;
            myCodeMirror.getDoc().setValue(myCode.trim());
            if (buttonId === 'code-modal') {
                myCodeMirror.setSize(null,300);
            }
        } else {
            area.style.display = 'none';
            showOrHide.innerHTML = showOrHide.innerHTML.replace('Hide', 'Show');
            if (bs3) {
                bs3.setAttribute('class', '');
            }
        }
    }
}


function handleOAuthResponse(res, oktaSignIn) {
    if (res[0]) {
        if (res[0].idToken)
            oktaSignIn.tokenManager.add('id_token', res[0]);
        else if (res[0].accessToken)
            oktaSignIn.tokenManager.add('access_token', res[0]);
    }
    if (res[1]) {
        if (res[1].idToken)
            oktaSignIn.tokenManager.add('id_token', res[1]);
        else if (res[1].accessToken)
            oktaSignIn.tokenManager.add('access_token', res[1]);
    }
    if (res.status === 'SUCCESS') {
        if (oktaSignIn.tokenManager.get('access_token'))
            get_profile('access_token', oktaSignIn.tokenManager.get('access_token').accessToken);
        else if (oktaSignIn.tokenManager.get('id_token'))
            get_profile('id_token', oktaSignIn.tokenManager.get('id_token').idToken);
    }
}