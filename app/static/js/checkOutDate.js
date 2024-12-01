document.addEventListener('DOMContentLoaded', function () {

      const checkInDate = document.getElementById('checkin-date');
      const nightsSelect = document.querySelector('select.form-select');
      const checkoutLabel = document.querySelector('label[for="checkout-date"]');

      function updateCheckoutDate() {
            const startDate = new Date(checkInDate.value);
            const nights = parseInt(nightsSelect.value);

            if (!isNaN(startDate.getTime() && nights)) {
                  const checkoutDate = new Date(startDate);
                  checkoutDate.setDate(startDate.getDate() + nights);

                  // Format date in Vietnamese
                  const formatter = new Intl.DateTimeFormat('en-US',
                        {
                              month: 'long',
                              day: 'numeric',
                              year: 'numeric'
                        }
                  );
                  checkoutLabel.textContent = formatter.format(checkoutDate);
            }
      }
      checkInDate.addEventListener('change', updateCheckoutDate);
      nightsSelect.addEventListener('change', updateCheckoutDate);

});


