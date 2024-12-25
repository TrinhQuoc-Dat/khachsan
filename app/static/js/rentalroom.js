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
            inputCustomer = document.getElementById('input-customer')
            inputCustomer.style.display = 'block';
            document.getElementById('input-cccd').style.display ='none'
            document.getElementById('nameb').value = data.customer.full_name
            document.getElementById('emailb').value = data.customer.email
            document.getElementById('phoneb').value = data.customer.phone
            document.getElementById('cccdb').value = data.customer.cccd
            console.log(data.customer)
        }else {
            inputCustomer = document.getElementById('input-customer')
            inputCustomer.classList.remove('display-none')
            inputCustomer.classList.add('display')
            document.getElementById('input-cccd').style.display ='none'
        }
    })
    .catch(err => console.log(err))
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