// thời gian kết thúc (YYYY-MM-DDTHH:MM:SS)
const endTime = new Date("2024-12-30T23:59:59").getTime();

function updateCountdown() {
      const now = new Date().getTime();
      const timeLeft = endTime - now;
      if (timeLeft > 0) {
            const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
            const hours = Math.floor(timeLeft % (1000 * 60 * 60 * 24) / (1000 * 60 * 60))
            const minutes = Math.floor(timeLeft % (1000 * 60 * 60) / (1000 * 60));
            const seconds = Math.floor(timeLeft % (1000 * 60) / 1000);

            document.getElementById("countdown").innerHTML = ` <span>${days}</span>
            <p>:</p>
            <span>${hours.toString().padStart(2, '0')}</span>
            <p>:</p>
            <span>${minutes.toString().padStart(2, '0')}</span>
            <p>:</p>
            <span>${seconds.toString().padStart(2, '0')}</span>`;
      } else {
            document.getElementById("countdown").innerHTML = "Chương trình đã kết thúc!";
      }
}

setInterval(updateCountdown, 1000);
updateCountdown();