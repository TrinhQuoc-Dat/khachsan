window.onload = function() {
      const ctx = document.getElementById('doanhThuChart');

new Chart(ctx, {
type: 'bar',
data: {
      labels: ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12'],
      datasets: [{
      label: 'Doanh thu hàng tháng',
      data: [12000, 15000, 17000, 21000, 43000, 20000, 39000, 15000, 20000, 25000, 30000, 35000],
      borderWidth: 1
      }]
},
options: {
      scales: {
      y: {
      beginAtZero: true
      }
      }
}
});

const ctx2 = document.getElementById('tanSuatChart');

new Chart(ctx2, {
type: 'line',
data: {
labels: ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12'],
datasets: [
      {
      label: 'Phòng thường',
      data: [12, 19, 3, 5, 2, 3, 6, 21, 1, 2, 3, 4],
      borderColor: 'rgb(75, 192, 192)', 
      borderWidth: 2,
      fill: false,
      tension: 0.1
      },
      {
      label: 'Phòng VIP',
      data: [5, 10, 4, 18, 2, 8, 5, 14, 9, 11, 12, 14],
      borderColor: 'red', 
      borderWidth: 2,
      fill: false,
      tension: 0.1
      }
]
},
options: {
scales: {
      y: {
      beginAtZero: true
      }
}
}
});

      }; 