
window.onload = function () {
      // Lấy ngữ cảnh từ phần tử canvas
      const ctx = document.getElementById('myChart').getContext('2d');

      // Tạo biểu đồ
      new Chart(ctx, {
            type: 'bar',
            data: {
                  labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                  datasets: [{
                        label: '# of Votes',
                        data: [12, 19, 3, 5, 2, 3],
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
};
