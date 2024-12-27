function addComment(roomId) {
    let comment = document.getElementById("commentId")
    let title = document.getElementById('title-new')
    let star = document.getElementById('star')
    fetch('/api/comment',{
          method: 'POST',
          body: JSON.stringify({
                'room_id': roomId,
                'title': title.value,
                'comment': comment.value,
                'star': star.value
          }),
          headers: {
                'Content-Type': 'application/json'
          }
    }).then(res => res.json()).then(data => {
          if (data.status == 201){
                let c = data.comment
                let area = document.getElementById('commentArea')
                area.innerHTML = `
                      <div class="row d-flex align-items-center mt-3 p-3"
                      style="border-bottom: 1px solid #cfd8e8;">
                      <div class="col-md-3">
                      <div class="row">
                            <div class="col-md-4 image-container">
                                  <img
                                  src="${ c.avatar }"
                                  alt="image user">
                            </div>
                            <div class="col-md-8">
                                  <div
                                  class="name">${ c.name }</div>
                                  <div
                                  class="date">${ c.created_date }</div>
                                  <div class="details">
                                  <span>🛏
                                         Phòng có ban công hướng núi...</span>
                                  <span>📅 2 đêm · tháng 8, 2024   gia đình</span>
                                  <span><i class="fa-solid fa-person"
                                              style="color: #FFD43B;"></i> <i
                                              class="fa-solid fa-person"
                                              style="color: #74C0FC;"></i>
                                           gia đình</span>
                                  </div>
                            </div>
                      </div>
                      </div>
                      <div class="col-md-9">
                      <h4>${c.title}</h4>
                      <div class="rating">
                            <span class="rating-score">${c.star}</span>
                            <span class="rating-text">Xuất sắc</span>
                      </div>
                      <p>
                            ${c.comment}
                      </p>
                      <div class="feedback useful-information">
                            <i class="fa-solid fa-thumbs-up like-comment"></i> Thích
                            Đánh giá này có hữu
                            ích với bạn không?
                      </div>
                      </div>
                </div>
                ` + area.innerHTML
          } else if (data.status == 404){
                alert(data.err_msg)
          }
    })

}
