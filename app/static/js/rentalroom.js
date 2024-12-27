let rentalCounter = 0;
let dataRoom = { rooms: [] };
let rentalData = []

function searchCustomer(obj){
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
            if (rentalCounter > 0){
            document.getElementById('name' + String(rentalCounter)).value = data.customer.full_name
            document.getElementById('email' + String(rentalCounter)).value = data.customer.email
            document.getElementById('phone' + String(rentalCounter)).value = data.customer.phone
            document.getElementById('cccd' + String(rentalCounter)).value = data.customer.cccd
            console.log(data.customer)
            }
            else {
                document.getElementById('name').value = data.customer.full_name
                document.getElementById('email').value = data.customer.email
                document.getElementById('phone').value = data.customer.phone
                document.getElementById('cccd').value = data.customer.cccd
                console.log(data.customer)
            }
        }
    })
    .catch(err => console.log(err))
}


function searchRoom(obj){
    let type ,dateIn
    if (rentalCounter > 0){
        type = document.getElementById('type' + String(rentalCounter)).value
        dateIn = document.getElementById('check_in_date' + String(rentalCounter)).value
    }else {
        type = document.getElementById('type').value
        dateIn = document.getElementById('check_in_date').value
    }
    const dateOut = obj.value

    if(dateIn && dateOut && (dateIn < dateOut)){
        fetch('/api/search-room-rental', {
            method: 'post',
            body: JSON.stringify({
                'type': type,
                'date-in': dateIn,
                'date-out': dateOut,
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json())
        .then(data => {
            if(data.code == 200){
                dataRoom.rooms = data.rooms
                let rooms = null;
                if (rentalCounter > 0){
                    rooms = document.getElementById('room' + String(rentalCounter))
                }else {
                rooms = document.getElementById('room')
                }
                html = ``;
                for (room of data.rooms){
                    html += `<option value="${room.id}">${room.name}</option>`
                }
                rooms.innerHTML = html;

                console.log(data.rooms)
            }else {
                document.getElementById('error-mess').classList.remove('display-none')
                document.getElementById('mess').innerText = data.mess
            }
        }).catch(err => console.log(err))
    }
}

function updateRoomPrice(obj) {
    const selectedRoomId = obj.value;
    const selectedRoom = dataRoom.rooms.find(room => room.id == selectedRoomId);

    if (selectedRoom) {
        id = ''
        if (rentalCounter > 0) id = rentalCounter
        const roomPriceElement = document.getElementById('room-price' + String(id));
        roomPriceElement.textContent = `${selectedRoom.price.toLocaleString()} VND`;
    } else {
        document.getElementById('room-price').textContent = '0 VND';
    }
}

function LapPhieuThue(id, customerId){
    let roomCustomers = []
    let selects = document.querySelectorAll('.form-select')

    selects.forEach(select => {
        let roomId = select.id.replace('number-customer', '') 
        let numberCustomer = select.value
        roomCustomers.push({
            'room_id': roomId,
            'number_customer': numberCustomer
        })
    })
    fetch('/api/lap-phieu-thue-phong', {
        method:'post',
        body: JSON.stringify({
            'booking_id': id,
            'customer-id': customerId,
            'rooms': roomCustomers,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
    .then(data => {
        if(data.code == 200){
            rentalsuccess = document.getElementById('rentalsuccess')
            rentalsuccess.classList.remove('display-none')
            document.getElementById('booking-rental').style.display = 'none'
        }
    }).catch(err => console.log(err))
}

function addRentalForm() {
    const rentalTemplate = document.querySelector('#add-rental').cloneNode(true);
    const inputs = rentalTemplate.querySelectorAll('input, select');
    const roomPrice = rentalTemplate.querySelector('#room-price')
    rentalCounter++;
    roomPrice.id = `${roomPrice.id}${rentalCounter}`
    inputs.forEach(input => {
        input.id = `${input.id}${rentalCounter}`;
        input.name = `${input.name}${rentalCounter}`;
        input.value = "";
    });
    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Xóa';
    deleteButton.className = 'btn btn-danger mt-2';
    deleteButton.type = 'button';
    deleteButton.onclick = function () {
        rentalTemplate.remove(); 
        rentalCounter--;
    };
    rentalTemplate.appendChild(deleteButton);
    document.querySelector('#rental-form').insertBefore(rentalTemplate, document.querySelector('.d-flex.justify-content-between'));
}



function addRentalData() {
    rentalData =[]
    for (let i = 0; i <= rentalCounter; i++){
        let id = ''
        if(i > 0){
            id = i
        }
        const checkInDate = new Date(document.getElementById('check_in_date' + String(id)).value)
        const checkOutDate = new Date(document.getElementById('check_out_date' + String(id)).value)
        roomId = document.getElementById('room'+ String(id)).value
        const selectedRoom = dataRoom.rooms.find(room => room.id == roomId);
        const price = selectedRoom ? selectedRoom.price : 0;
        const days = Math.ceil((checkOutDate - checkInDate) / (1000 * 60 * 60 * 24))
        const numberCustomer = document.getElementById('number-cus' + String(id)).value
        let totalAmount = price * days 
        if (numberCustomer == 3){
            totalAmount *= 1.25
        }
        let rentalItem = {
            customer: {
                cccd: document.getElementById('cccd' + String(id)).value,
                name: document.getElementById('name' + String(id)).value,
                phone: document.getElementById('phone' + String(id)).value,
                email: document.getElementById('email'+ String(id)).value,
                typeCustomer: document.getElementById('type-customer' + String(id)).value
            },
            room: {
                type: document.getElementById('type' + String(id)).value,
                check_in_date: checkInDate,
                check_out_date: checkOutDate,
                room_id: roomId,
                number_customer: numberCustomer,
                total_amount: totalAmount,
            }
        }
        rentalData.push(rentalItem)
    }
    return rentalData
}



function addRental(){
    if (confirm('Xác nhận lập phiếu thuê Phòng !!!') == true){
        rentalData = addRentalData()
        console.log(rentalData)
        fetch('/api/add-rental-receipt', {
            method: 'post',
            body:JSON.stringify({
                'data': rentalData
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json())
        .then(data => {
            if (data.code == 200)
                location.reload()
        }).catch(err => console.log(err))
    }
}