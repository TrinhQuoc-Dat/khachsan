const monthPicker = document.getElementById('monthPicker');
const tableBody = document.querySelector(".report-table tbody");
const chartCtx = document.getElementById("myChart").getContext("2d");

let chart = null;

// Lấy tháng năm mặc định khi load trang
const currentDate = new Date();
const defaultMonth = currentDate.toISOString().slice(0, 7);
monthPicker.value = defaultMonth;

function fetchAndUpdateStats(month, year) {
      fetch('/api/frequency', {
            method: 'POST',
            headers: {
                  'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                  month: parseInt(month),
                  year: parseInt(year)   
            })
      })
            .then(response => {
                  if (!response.ok) {
                        throw new Error('Network response was not ok');
                  }
                  return response.json();
            })
            .then(data => {
                  // Cập nhật bảng
                  updateTable(data);
                  // Cập nhật biểu đồ
                  updateChart(data);
            })
            .catch(error => {
                  console.error('Error:', error);
                  alert('Có lỗi xảy ra khi tải dữ liệu');
            });
}

function updateTable(data) {
      let tableContent = "";

      data.forEach((row, index) => {
            const usageRate = parseFloat(row.usage_rate).toFixed(1);
            tableContent += `
                  <tr>
                  <td>${index + 1}</td>
                  <td>${row.room_name}</td>
                  <td>${row.days_rented}</td>
                  <td>${usageRate}%</td>
                  </tr>
            `;
      });

      tableBody.innerHTML = tableContent;
}

function updateChart(data) {
      // Xóa chart cũ nếu tồn tại
      if (chart) {
            chart.destroy();
      }
       // Tạo mảng các nhãn cho biểu đồ từ dữ liệu (tên các phòng)
      const labels = data.map(row => row.room_name);
      // Tạo mảng tỷ lệ sử dụng (usage rate) của các phòng từ dữ liệu
      const usageRates = data.map(row => parseFloat(row.usage_rate));

      chart = new Chart(chartCtx, {
            type: 'bar',
            data: {
                  labels: labels,
                  datasets: [{
                        label: 'Tỷ lệ sử dụng phòng (%)',
                        data: usageRates,
                        backgroundColor: [`rgba(214, 236, 250, 1)`, `rgba(53, 195, 121, 1)`,`rgba(235, 224, 255, 1)`,`rgba(237, 206, 212,1)`, `rgba(255, 245, 220, 1)`],
                        borderColor: [`rgba(214, 236, 2250, 2)`, `rgba(53, 195, 121, 2)`,`rgba(235, 224, 255, 2)`,`rgba(237, 206, 212, 2)`, `rgba(255, 245, 220, 1)`],
                        borderWidth: 1
                  }]
            },
            options: {
                  responsive: true,
                  scales: {
                        y: {
                              beginAtZero: true,
                              max: 100
                        }
                  }
            }
      });
}

// Event listener cho monthPicker
monthPicker.addEventListener('change', (event) => {
      const selectedMonth = event.target.value;
      const [year, month] = selectedMonth.split("-");
      console.log(`Tháng được chọn: ${month} năm ${year}`);
      fetchAndUpdateStats(month, year);
});

// Khởi tạo dữ liệu ban đầu
fetchAndUpdateStats(currentDate.getMonth() + 1, currentDate.getFullYear());