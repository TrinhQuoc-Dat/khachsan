
const yearSelector = document.getElementById('yearSelector');


const startYear = 2000;
const endYear = new Date().getFullYear();


for (let year = startYear; year <= endYear; year++) {
      const option = document.createElement('option');
      option.value = year;
      option.textContent = year;
      yearSelector.appendChild(option);
}

yearSelector.addEventListener('change', (event) => {
      console.log(`Selected Year: ${event.target.value}`);
});
