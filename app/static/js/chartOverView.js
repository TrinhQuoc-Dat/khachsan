async function loadRevenueData() {
      try {
            const response = await fetch('/api/overview');
            const data = await response.json();

            // Cập nhật bảng
            const tableBody = document.querySelector('#revenueTable tbody');
            tableBody.innerHTML = data.map(item => `
                  <tr>
                        <td>Tháng ${item.month}</td>
                        <td>${new Intl.NumberFormat('vi-VN').format(item.revenue)} VND</td>
                  </tr>
            `).join('');
            
            function getRandomColor() {
                  const r = Math.floor(Math.random() * 256);
                  const g = Math.floor(Math.random() * 256);
                  const b = Math.floor(Math.random() * 256);
                  return `rgba(${r}, ${g}, ${b}, 0.7)`;
            }
            const backgroundColors = data.map(() => getRandomColor());

            // Tạo biểu đồ
            const ctx = document.getElementById('myChart').getContext('2d');
            new Chart(ctx, {
                  type: 'polarArea',
                  data: {
                        labels: data.map(item => `Tháng ${item.month}`),
                        datasets: [{
                              label: 'Doanh thu theo tháng (VND)',
                              data: data.map(item => item.revenue),
                              backgroundColor: backgroundColors,
                              borderColor: 'rgba(54, 162, 235, 1)',
                              borderWidth: 1
                        }]
                  },
                  options: {
                        responsive: true,
                        scales: {
                              y: {
                                    display: false
                              }
                        },
                        plugins: {
                              tooltip: {
                                    callbacks: {
                                          label: function (context) {
                                                return new Intl.NumberFormat('vi-VN').format(context.raw) + ' VND';
                                          }
                                    }
                              }
                        }
                  }
            });
      } catch (error) {
            console.error('Error loading revenue data:', error);
      }
}

// Load data when page loads
document.addEventListener('DOMContentLoaded', loadRevenueData);
