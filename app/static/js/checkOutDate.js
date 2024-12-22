
window.onload = () =>{
      const checkinDateInput = document.getElementById('checkin-date');
      const today = new Date().toISOString().split('T')[0];   
      checkinDateInput.value = today;
      }

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

                  // Định dạng ngày tháng năm theo kiểu Việt Nam
                  const formatter = new Intl.DateTimeFormat('vi-VN', {
                        day: 'numeric',
                        month: 'numeric',
                        year: 'numeric'
                  });
                  checkoutLabel.textContent = formatter.format(checkoutDate);
            }
      }

      checkInDate.addEventListener('change', updateCheckoutDate);
      nightsSelect.addEventListener('change', updateCheckoutDate);
});
