$(document).ready(function() {
    $(".logout").hide();
    var selectedValue;
    $('input[name="inlineRadioOptions"]').on('change', function() {
        selectedValue = $('input[name="inlineRadioOptions"]:checked').val();
        //console.log("Selected value: " + selectedValue);
    });
  $('#myForm').submit(function(event) {
      event.preventDefault(); // Prevent form submission

      var formData = new FormData(); // Create a FormData object

      // Append the form fields to the FormData object
      formData.append('name', $('#name').val());
      formData.append('itemName', $('#itemName').val());
      formData.append('contact', $('#contact').val());
      formData.append('location', $('#locationn').val());
      formData.append('date', $('#date').val());
      formData.append('statusType', selectedValue); // Use the selectedValue variable;

      // Append the image file to the FormData object
      // Handle the file input
      var imageInput = $('#image')[0].files[0];
        if (imageInput) {
        formData.append('image', imageInput);
        } else {
        // If no file is uploaded, use the default value
        formData.append('image', $('#defaultImage').val());
        }

      $.ajax({
          url: '/upload/',
          method: 'POST',
          data: formData,
          contentType: false, // Prevent jQuery from setting content type
          processData: false, // Prevent jQuery from processing the data
          success: function(response) {
              //console.log(response);
          },
          error: function(error) {
              //console.log('Error:', error);
          }
      });
      alert("Done!")
      // Reset the form items
      document.getElementById("myForm").reset();
  });
});
