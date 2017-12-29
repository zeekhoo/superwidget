var url = 'https://'  + org;  //eg https://zeekhoo.okta.com

var oktaSignIn = new OktaSignIn({
    baseUrl: url
});

oktaSignIn.session.get(function (res) {
    if (res.status === 'ACTIVE') {
        oktaSignIn.session.close(function (err) {
            if (err) {
                console.log(err);
                return;
            } else {
                console.log('logged out successfully');
            }
        });
    }
})
