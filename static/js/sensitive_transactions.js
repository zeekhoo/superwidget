var xfer_config = {
  url: 'https://[[org]]',
  //grantType: 'authorization_code', Need to upgrade SDK for this.
  issuer: '[[iss]]',
  clientId: '[[money_xfer_oidc_client_id]]'
};

var oidc_config = {
  scopes: ['high_value_cash_xfer'],
  responseType: 'token',
  nonce:'device_id_fingerprint',
}
var authXferClient = new OktaAuth(xfer_config);

function post_transfer(amount) {
    data = {}
    var access_token_parts = srv_access_token.split('.');
    var existingAccessToken = JSON.parse(window.atob(access_token_parts[1]));

    $('#access_token_subject').html('')
    $('#access_token_xfer_auth').html('')
    $('#access_token_xfer_auth_message').html('')
    //Let's check locally to see if our normal token will work or not.
    if(existingAccessToken.xfer_auth_amount < amount) {
      authXferClient.token.getWithPopup(oidc_config)
      .then(function(tokenOrTokens) {
        accessToken = tokenOrTokens.accessToken;
        $.ajax({
            url: '/transfer',
            method: 'POST',
            data: {"amount": amount},
            beforeSend: function (xhr) {
                xhr.setRequestHeader("Authorization", "Bearer " + accessToken);
            },
            success: function(res) {
              console.log(res.Message)
              alert(res.Message);
            },
            error: function(res) {
              alert(res.responseJSON.Message);
            }
        });
        $('#access_token_subject').html("User: " + authXferClient.token.decode(accessToken).payload.sub);
        $('#access_token_xfer_auth').html("Authorized Amount: " + authXferClient.token.decode(accessToken).payload.xfer_auth_amount);
        if(authXferClient.token.decode(accessToken).payload.xfer_auth_message) {
          $('#access_token_xfer_auth_message').html("Fraud System Adjustments: " + authXferClient.token.decode(accessToken).payload.xfer_auth_message);
        }
      })

      .catch(function(err) {
        console.log(err)
        alert("This user has not been authorized to transfer money. Message: " + err.message);
      })
      .finally(function() {
        $('#amount').val('');
        $('#from').val('');
        $('#to').val('');
      });
    }
    else {
      $.ajax({
          url: '/transfer',
          method: 'POST',
          data: {"amount": amount},
          beforeSend: function (xhr) {
              xhr.setRequestHeader("Authorization", "Bearer " + srv_access_token);
          },
          success: function(res) {
            console.log(res.Message)
            alert(res.Message);
            $('#access_token_subject').html("User: " + existingAccessToken.sub);
            $('#access_token_xfer_auth').html("Authorized Amount: " + existingAccessToken.xfer_auth_amount);
          },
          error: function(res) {
            alert(res.responseJSON.Message);
          }
      });
    }


}
