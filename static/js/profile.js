function prettyPrint(ugly) {
    var obj = JSON.parse(ugly);
    return JSON.stringify(obj, undefined, 4);
}

document.getElementById('profile_pretty').innerHTML = prettyPrint(profile);

function openInNewTab(url) {
  var win = window.open(url, '_blank');
  win.focus();
}

function app_b() {
    var client_id = '0oa4ox4jzjHj9vWgR1t7';
    var redirectUri = 'http%3A%2F%2Flocalhost%3A8000%2Foauth%2Fcallback';

    var auth_url = 'https://zeekhoo.okta.com/oauth2/ausxkcyonq9Ht1uvi1t6/v1/authorize';

    var url = auth_url
        + '?response_type=id_token+token'
        + '&client_id=' + client_id
        + '&scope=openid+profile+phone'
        + '&redirect_uri=' + redirectUri
        + '&state=foo'
        + '&nonce=foo';

    openInNewTab(url);
}