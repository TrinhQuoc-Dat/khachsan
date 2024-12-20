window.onload = () => {
      const checkinDateInput = document.getElementById('checkin-date');
      const today = new Date().toISOString().split('T')[0];
      checkinDateInput.value = today;
}
