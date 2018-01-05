var url = 'https://'  + org;  //eg https://login.alwaysaasure.com

var oktaSignIn = new OktaSignIn({
    baseUrl: url
});

oktaSignIn.session.get(function (res) {
    if (res.status === 'ACTIVE') {
        //clear tokens from local storage
        oktaSignIn.tokenManager.clear();

        oktaSignIn.session.close(function (err) {
            if (err) {
                console.log(err);
                return;
            } else {
                console.log('logged out successfully');
                window.location.href = "/";
            }
        });
    }
})
