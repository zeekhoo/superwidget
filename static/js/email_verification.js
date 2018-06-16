
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
    },
});


function toggleEmailField() {
    var state = verificationApp.state;

    switch(state) {
        case 'verify-email':
            verificationApp.state = 'verify-token';
            break;
        case 'verify-token':
            verificationApp.state = 'set-password';
            break;
    }

    var form = document.getElementById('emailActivationForm');
    if (form) {
        form.state.value = verificationApp.state;
        form.submit();
    }
}