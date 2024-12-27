
function deleteRoom(idRoom){
    fetch('/api/delete-room', {
        method: 'post',
        body: JSON.stringify({
            'id': idRoom
        }),
        headers:{
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
    .then(data => {
        const total_room = document.getElementById('total-room')
        const room = document.getElementById('room'+ idRoom)
        const roomDelete = document.getElementById('room-delete' + idRoom)
        const cartCounter = document.getElementById('cartCounter')
        
        const giaSoc = document.getElementById('gia-soc')
        const uuDai = document.getElementsByClassName('uu-dai')
        const tong = document.getElementById('tong')

        const formattedAmount = new Intl.NumberFormat('vi-VN', {
            style: 'decimal',
            currency: 'VND'
        })
        giaSoc.innerText = formattedAmount.format(data.mess.total_amount) + 'VND';
        tong.innerText = formattedAmount.format(data.mess.total_amount * 0.9) + 'VND';
  
        for (let i = 0; i < uuDai.length; i++) {
            uuDai[i].innerText = formattedAmount.format(data.mess.total_amount * 0.1) + 'VND';
        }
        cartCounter.innerText = data.mess.total_quantity
        room.style.display = 'none';
        total_room.innerText = data.mess.total_quantity + ' phòng lớn';
        roomDelete.style.display = 'none';
    }).catch(err => console.error(err))
}


function searchCustomer(obj, idRoom){
    fetch('/api/search-customer', {
        method: 'post',
        body: JSON.stringify({
            'id': obj.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
    .then(data => {
        if(data.code == 200 ){
            console.log(data.customer)
            if (idRoom == 0){
                idRoom = ''
            }else {
                document.getElementById('type-customer' + String(idRoom)).value = data.customer.type_customer
            }
            document.getElementById('name' + String(idRoom)).value = data.customer.full_name
            document.getElementById('email' + String(idRoom)).value = data.customer.email
            document.getElementById('phone' + String(idRoom)).value = data.customer.phone
            document.getElementById('cccd' + String(idRoom)).value = data.customer.cccd
        }
    })
    .catch(err => console.log(err))
}

function checkEmail(input) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(input);
}
function isValidCCCD(cccd) {
    const cccdRegex = /^\d{12}$/;
    return cccdRegex.test(cccd);
}
function isValidPhoneNumber(phone) {
    const phoneRegex = /^(0[3-9]{1}[0-9]{8})$/;
    return phoneRegex.test(phone);
}


// function EventCheckMail(e) {
//     if (e.value == '') return;
//     if (!checkEmail(e.value)) {
//         errorMgs.innerHTML = 'Mail không tồn tại!!!';
//         document.getElementById('error-mail').style.display = 'block';
//     } else {
//         errorMgs.innerHTML = '';
//         document.getElementById('error-mail').style.display = 'none';
//     }
// }