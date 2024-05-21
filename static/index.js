document.addEventListener('DOMContentLoaded', function () {
  var form = document.querySelector('form');
  var modeElement = document.querySelector('.mode');

  form.addEventListener('submit', function (event) {
      event.preventDefault(); // Prevents the form from submitting

      // Get the selected radio button value
      var selectedOption = document.querySelector('input[name="options"]:checked');
      if (selectedOption) {
          // Update the text of the mode element
          modeElement.textContent = 'Selected Mode: ' + selectedOption.value;
      }
  });
});