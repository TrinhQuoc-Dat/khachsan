
const monthPicker = document.getElementById('monthPicker');


const currentDate = new Date();
const defaultMonth = currentDate.toISOString().slice(0, 7);
monthPicker.value = defaultMonth;

monthPicker.addEventListener('change', (event) => {
      console.log("Tháng được chọn:", event.target.value);
});
