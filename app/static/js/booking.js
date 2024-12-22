document.addEventListener('DOMContentLoaded', function() {
    let search = document.getElementById('search')
    search.addEventListener('click', () =>{
        get_room()
    })
});
window.onload = () =>{
    const checkinDateInput = document.getElementById('checkin-date');
    const today = new Date().toISOString().split('T')[0];   
    checkinDateInput.value = today;
}

function get_room(){
    const name = document.getElementById('location').value
    let dateIn =  document.getElementById('checkin-date').value
    const day = parseInt(document.getElementById('overnight').value, 10);
    const typeRoom = document.getElementById('type-room').value
    let dateOut;

    if (!dateIn) {
        const today = new Date();
        dateIn = today.toISOString().split('T')[0]; 
    }

    dateIn = new Date(dateIn);
    dateOut = new Date(dateIn);
    dateOut.setDate(dateOut.getDate() + day);
    const formatter = new Intl.DateTimeFormat('vi-VN', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
    const formattedDateOut = formatter.format(dateOut);
    const formattedDateIn = formatter.format(dateIn);

    fetch('/api/booking/search-room',{
        method : 'post',
        body: JSON.stringify({
            "nameRoom" : name,
            "dateIn": formattedDateIn,
            "dateOut": formattedDateOut,
            "typeRoom": typeRoom
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json())
    .then(data => {
        if (data.code == 200){
            console.log(data.rooms)
            const roomSearch = document.getElementById('room-search');
            let areaRoom = ``;
            for(let r of data.rooms){
                areaRoom += ` <div class="mt-2">
                <div class="border-booking">
                    <div class="d-flex p-3">
                        <div class="item-2 p-1 me-3 container-image">
                            <img src="${r.image }" alt="Khach san" class="mr-2">
                        </div>
                        <div class="d-flex flex-column item-7">
                            <div class="d-flex  header-title">
                                <div class="d-flex flex-column">
                                    <div>
                                        <h3 class="m-0 text-color-blue">Khách Sạn Oasia</h3>
                                        <div class="stats"></div>
                                        <span></span>
                                    </div>
                                    <div>
                                        <span class="text-small">Cách trung tâm 3km</span>
                                    </div>
                                </div>
                                <div class="d-flex align-items-space">
                                    <div>
                                        <h5 class="m-0">Tuyệt hảo</h5>
                                        <span class="text-color-stap"><a href="#" style="all: unset;">99 đánh giá <i
                                                    class="fa-solid fa-star" style="color: #FFD43B;"></i></a></span>
                                    </div>
                                    <div>
                                        <div>
                                            <span class="border-three-corners text-color-write">9.5</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="mt-2">
                                <div>
                                    <span class="bg-color-green  text-color-write p-1 text-center rounded">Ưu đãi cuối
                                        năm</span>
                                </div>
                            </div>
                            <div class="">
                                <div class="d-flex header-title">
                                    <div class="mt-1">
                                        <h5>${r.name }</h5>
                                        <ul class="no-bullet m-0 p-0">
                                            <li>
                                                <span class="text-small">1 giường đôi lớn</span>
                                            </li>
                                            <li>
                                                <div class="d-flex align-items-space">
                                                    <div><i class="fa-solid fa-check color-green"></i></div>
                                                    <div><span class="text-small color-green">Miễn phí hủy</span></div>
                                                </div>
                                                <div class="d-flex align-items-space">
                                                    <div><i class="fa-solid fa-check color-green"></i></div>
                                                    <div><span class="text-small color-green">Không cần thanh toán online -
                                                            Thanh toán tại chỗ nghỉ</span></div>
                                                </div>
                                                <div>
                                                    <span class="text-small text-color-stap text-color-red">Chỉ còn 4 phòng
                                                        với giá này trên trang của chúng tôi</span>
                                                </div>
                                            </li>
                                        </ul>
                                    </div>
                                    <div class="text-aline-right">
                                        <span class="text-small">1 đêm 2 người lớn</span>
                                        <br>
                                        <span class="text-color-discount">${ new Intl.NumberFormat('vi-VN').format(r.price) } VND</span>
                                        <h3>${  new Intl.NumberFormat('vi-VN').format( r.price *0.9) } VND</h3>
                                        <span class="text-small">Đã bao gồm thuế và phí</span>
                                        <hr>
                                        <input type="button" onclick="add_cart('${String(r.id)}' ,'${r.name}', '${String(r.price)}', '${r.type_room}', '${r.image}')" value="Chọn phòng" name="booking" class="btn btn-success" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>`
            }
            roomSearch.innerHTML = areaRoom;
        }else {
            if(data.code == 404) 
                alert(data.error)
        }
    }).catch(err => console.error(err))
}


function add_cart(id ,name, price, typeRoom, image){

    let dateIn =  document.getElementById('checkin-date').value
    const day = parseInt(document.getElementById('overnight').value, 10);
    let dateOut;

    if (!dateIn) {
        const today = new Date();
        dateIn = today.toISOString().split('T')[0]; 
    }

    dateOut = new Date(dateIn);
    dateOut.setDate(dateOut.getDate() + day);
    const formatter = new Intl.DateTimeFormat('vi-VN', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
    const formattedDateOut = formatter.format(dateOut);
    let numberCustomer = document.getElementById('number-customer').value
    
    fetch('/api/add-room-cart', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': Number(price),
            'image': image,
            'type-room': typeRoom,
            'number-customer': Number(numberCustomer),
            'date-in':dateIn,
            'date-out': formattedDateOut,
            'day': day,
        }),
        headers:{
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
    .then(data => {
        if (data.code == 300){
            let cartCounter = document.getElementById('cartCounter');
            cartCounter.innerText = data.mess.total_quantity;
            alert('Thêm Phòng Thành công!!!')
        }
        else {
            alert(data.mess)
        }
    }).catch(err => console.error(err))
}

