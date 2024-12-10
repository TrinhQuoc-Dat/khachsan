document.addEventListener('DOMContentLoaded', () => {
      const likeButtons = document.querySelectorAll('.like-comment');

      likeButtons.forEach(like => {
            like.addEventListener('click', () => {
                  like.classList.toggle('liked'); 
            });
      });
});