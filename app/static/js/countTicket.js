document.addEventListener('DOMContentLoaded', function(){
      const ticket = document.querySelectorAll(".ticket");
      const countTicket = document.getElementById("count-ticket")
      countTicket.textContent = ticket.length;
})