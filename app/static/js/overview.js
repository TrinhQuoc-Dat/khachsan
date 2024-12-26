document.addEventListener("DOMContentLoaded", function () {
      fetch('/api/overview')
            .then(response => {
                  if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                  }
                  return response.json();
            })
            .then(data => {
                  if (data.error) {
                        console.error('API Error:', data.error);
                        return;
                  }

                  // Gán giá trị vào giao diện
                  document.querySelector(".Overview .card:nth-child(3) h2").innerText = data.current_guests;
                  document.querySelector(".Overview .card:nth-child(4) h2").innerText = data.booking_today; // Đồng bộ tên key
                  document.querySelector(".Overview .card:nth-child(5) h2").innerText = `${data.month_revenue.toLocaleString()} VNĐ`;
            })
            .catch(error => {
                  console.error('Error fetching data:', error);
            });
});