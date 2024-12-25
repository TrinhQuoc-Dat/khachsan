function loadRevenueStats(monthValue) {
      const [year, month] = monthValue.split('-');

      fetch('/api/revenue', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ month: parseInt(month), year: parseInt(year) })
      })
            .then(res => res.json())
            .then(data => {
                  const tbody = document.querySelector('tbody');
                  const total = data.normal.total_revenue + data.vip.total_revenue;

                  tbody.innerHTML = `
              <tr>
                  <td>1</td>
                  <td>${data.normal.type_room}</td>
                  <td>${new Intl.NumberFormat('vi-VN').format(data.normal.total_revenue)}</td>
                  <td>${data.normal.rental_count}</td>
                  <td>${((data.normal.total_revenue / total) * 100).toFixed(1)}%</td>
              </tr>
              <tr>
                  <td>2</td>
                  <td>${data.vip.type_room}</td>
                  <td>${new Intl.NumberFormat('vi-VN').format(data.vip.total_revenue)}</td>
                  <td>${data.vip.rental_count}</td>
                  <td>${((data.vip.total_revenue / total) * 100).toFixed(1)}%</td>
              </tr>
          `;

                  document.querySelector('tfoot td').innerHTML =
                        `Tổng doanh thu: ${new Intl.NumberFormat('vi-VN').format(total)}`;
                  document.querySelector('p.text-center').innerHTML =
                        `Tháng: ${month}/${year}`;
                  let myChart = null;
                  const chartData = [
                        data.normal.total_revenue || 0,
                        data.vip.total_revenue || 0
                  ];
                  const chartLabels = ['Phòng thường', 'Phòng VIP'];

                  const oldCanvas = document.getElementById('myChart');
                  const parent = oldCanvas.parentNode;
      
                  const newCanvas = document.createElement('canvas');
                  newCanvas.id = 'myChart';
                  parent.replaceChild(newCanvas, oldCanvas);

                  myChart = draw(document.getElementById('myChart'), chartData, chartLabels);
            });
}

function draw(ctx, data, labels) {
      return new Chart(ctx, {
            type: 'doughnut',
            data: {
                  labels: labels,
                  datasets: [{
                        label: 'Doanh thu loại phòng theo tháng',
                        data: data,
                        borderWidth: 1,
                        backgroundColor: [`rgba(50, 70, 80, 0.4)`, `rgba(53, 195, 121,0.9)`]
                        
                  }]
            },
            options: {
                  responsive: true,
                  maintainAspectRatio: false,
                  scales: {
                        y: {
                              beginAtZero: true
                        }
                  }
            }
      });
}

monthPicker.addEventListener('change', (event) => {
      loadRevenueStats(event.target.value);
});

loadRevenueStats(monthPicker.value);