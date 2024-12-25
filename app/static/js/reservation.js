
function deleteBookingDetail(id){
    if (confirm("Bạn có muốn hủy đặt phòng !!!") == true){
        fetch('/api/delete-booking-detail/' + id, {
            method: 'DELETE',
        }).then(res => res.json())
        .then(data => {
            if(data.code == 200){
                bookingDetail = document.getElementById('booking-detail' + id)
                bookingDetail.style.display = 'none'
            }else {
                alert(data.error)
            }
        })
        .catch(error => console.log(error))
    }
}

window.onload = function (){
    let date = document.getElementsByClassName('date')
    for (let i = 0; i < date.length; i++){
        date[i].innerText = moment(date[i].innerText).format('DD/MM/YYYY');
    }
    let myDate = document.getElementsByClassName('my-date')
    for (let i = 0; i < myDate.length; i++){
        myDate[i].innerText = moment(myDate[i].innerText).locale('vi').fromNow()
    }
}