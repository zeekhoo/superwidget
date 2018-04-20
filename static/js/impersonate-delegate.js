function impersonate(loginAs) {
    var authClient = new OktaAuth({url: 'https://[[impersonation_org]]'});

    var accessToken = '';
    if (srv_access_token != '') {
        //get the accessToken from session if it exists
        accessToken = srv_access_token;
    } else if (authClient.tokenManager.get('accessToken')) {
        //get the accessToken stored in local storage
        accessToken = authClient.tokenManager.get('accessToken').accessToken;
    }

    //Call some API that takes the input argument "loginAs" and then
    //1) Copies the profile over as a "shadow user" to the 2nd Okta org,
    //2) then, in the 1st Org, sets the "Application Credentials for Assigned User" (see https://developer.okta.com/docs/api/resources/apps#update-application-credentials-for-assigned-user)
    //to the same value. With this value set, the currently logged-in user assumes the username of another user (the loginAs user)
    //and via SAML, can login to the 2nd Okta org as different user
    $.ajax({
        url: '/set-name-id',
        method: 'POST',
        data: 'nameid='+loginAs,
        contentType: 'application/x-www-form-urlencoded',
        crossDomain: true,
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Authorization", "Bearer " + accessToken);
        },
        statusCode: {
            200: function(xhr) {
                //---------------------------------------------------------------------------------
                //This flow is based on https://developer.okta.com/authentication-guide/saml-login/
                //---------------------------------------------------------------------------------
                //With this one url:
                //1) Initiates SAML from Org#1 to Org#2
                //2) SAML logs the user into Org#2. But is logged in as "loginAs" username
                //3) Org#2 produces the OAuth tokens for the "loginAs" user
                //This url is produce per following guide:
                //https://developer.okta.com/authentication-guide/saml-login/#create-the-authorization-url
                var link = 'https://[[impersonation_org]]/oauth2/[[impersonation_org_auth_server_id]]/v1/authorize' //This 2nd Okta org's Auth Server produces tokens
                      + '?client_id=[[impersonation_org_oidc_client_id]]'
                      + '&scope=openid+profile+email'
                      + '&response_mode=fragment'
                      + '&idp=[[impersonation_org_redirect_idp_id]]' //redirects to 1st Okta org for authentication
                      + '&response_type=id_token+token'  //implicit grant (for SPA)
                      + '&redirect_uri=http://localhost:8000/login-delegate'  //redirect tokens to SPA endpoint for handling
                      + '&state=foo'
                      + '&nonce=foo'
                window.location.href = link;
            }
        }
    });
}

