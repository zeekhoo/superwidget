var data = [];
var verificationApp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#vueapp',
    data: {
        state: state,
        email: false,
        token: false,
        password1: false,
        password2: false
    }
});

function vueController() {
    var form = document.getElementById('fakeForm');
    if (form) {
        var state = verificationApp.state;
        console.log(state);
        switch (state) {
            case 'verify-email':
                verificationApp.state = 'verify-token';
                verificationApp.email = form.inputEmail.value;
                break;
            case 'verify-token':
                verificationApp.state = 'set-password';
                break;
            case 'set-password':
                break;
        }
    }
}



function toggleEmailField() {
    var form = document.getElementById('emailActivationForm');
    if (form) {
        form.submit();
    }
}
