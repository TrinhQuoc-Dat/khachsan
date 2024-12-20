
window.onload = function () {
      // Lấy ngữ cảnh từ phần tử canvas
      const ctx = document.getElementById('myChart').getContext('2d');
      
      // Tạo biểu đồ
      new Chart(ctx, {
            type: 'bar',
            data: {
            labels: ['Phòng thường', 'Phòng VIP'],
            datasets: [
                  {
                        label: 'Doanh thu',
                        data: [44, 5], // Dữ liệu doanh thu
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1,
                        yAxisID: 'y1',
                  },
                  {
                        label: 'Số lượt thuê',
                        data: [36, 48], // Dữ liệu số lượt thuê
                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1,
                        yAxisID: 'y2',
                  },
            ],
            },
            options: {
            responsive: true,
            scales: {
                  y1: {
                        type: 'linear',
                        position: 'left',
                        beginAtZero: true,
                        title: {
                        display: true,
                        text: 'Doanh thu (triệu)',
                        },
                  },
                  y2: {
                        type: 'linear',
                        position: 'right',
                        beginAtZero: true,
                        title: {
                        display: true,
                        text: 'Số lượt thuê',
                        },
                        grid: {
                        drawOnChartArea: false,
                        },
                  },
            },
            plugins: {
                  legend: {
                        display: true,
                        position: 'top',
                  },
            },
            },
      });
};
