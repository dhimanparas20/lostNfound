$(document).ready(function() {
  $('#Form').submit(function(event) {
      event.preventDefault(); // Prevent form submission

      var formData = new FormData(); // Create a FormData object

      // Append the form fields to the FormData object
      formData.append('uname', $('#uname').val());
      formData.append('passw', $('#password').val());

      $.ajax({
          url: '/login/',
          method: 'POST',
          data: formData,
          contentType: false, // Prevent jQuery from setting content type
          processData: false, // Prevent jQuery from processing the data
          success: function(response) {
              //console.log(response.message);
              if (response.message == "LoginFailed"){
                $('#message').text("Invalid User or Password. Try again");
              }
              else if(response.message == "LoginSuccessful"){
                window.location.href = "/";
              }
          },
          error: function(error) {
              console.log('Error:', error);
          }
      });
      // Reset the form items
      //document.getElementById("Form").reset();
  });
});
