function searchRental(){
    let name = document.getElementById('inputname').value
    if (name.trim() !== ''){
        fetch('/api/search-rental',{
            method: 'post',
            body: JSON.stringify({
                'name': name
            }),
            headers:{
                'Content-Type': 'application/json'
            }
        }).then(res => res.json())
        .then(data => {
            if (data.code == 200 ){
                console.log(data.rental)
                html = ``
                receiptPayment = document.getElementById('receipt-payment')
                for (receiptId in data.rental){
                    let receipt = data.rental[receiptId];

                    html += `<div class="border-booking p-3 mt-2">
                                <div>
                                    <h3 class="text-danger text-center">Hóa đơn thanh toán</h3>
                                </div>
                                <div>
                                    <div>
                                        <h5>Phiếu Thuê Phòng ID: ${receipt.rental_receipt.id}</h5>
                                        <p>Ngày tạo:  ${receipt.rental_receipt.created_date}</p>
                                    </div>
                                </div>
                                <div>
                                    <table class="table">
                                        <tr>
                                            <th>Mã</th>
                                            <th>Tên khách hàng</th>
                                            <th>Tên phòng</th>
                                            <th>Ngày nhận phòng</th>
                                            <th>Ngày trả phòng</th>
                                            <th>Số tiền </th>
                                        </tr>`;

                    receipt.details.forEach(detail => {
                        html += `
                        <tr>
                            <td>${detail.receipt_detail.id}</td>
                            <td>${detail.customer.full_name}</td>
                            <td>${detail.room.name}</td>
                            <td>${detail.receipt_detail.date_in}</td>
                            <td>${detail.receipt_detail.date_out}</td>
                            <td>${detail.receipt_detail.total_amount} VND</td>
                        </tr>`
                    });
                    html += `</table></div>`
                    html += `<div class="d-flex justify-content-between">
                                <div class="d-flex align-items-center">
                                    <div><h4>Tổng Tiền: </h4></div> 
                                    <div><h4 class="text-danger mb-1 p-2">${receipt.rental_receipt.total_amount} VND</h4 ></div>
                                </div>
                                <div>
                                    <input type="button" onclick="payment(${receipt.rental_receipt.customer_id},${receipt.rental_receipt.id}, ${receipt.rental_receipt.total_amount})" class="btn btn-danger" value="Xác nhận thanh toán"/>
                                </div>
                            </div> </div>`
                }
                receiptPayment.innerHTML = html;
            }else {
                document.getElementById('alert').classList.remove('display-none')
                document.getElementById('alert-error').innerText = data.error
            }

        }).catch(err => console.log(err))
    }
}

function payment(customerId, rentalReceiptId, amount){
    if (confirm('Xác nhận thanh toán !!!') == true){
        fetch('/api/payment', {
            method: 'post',
            body: JSON.stringify({
                'customer-id': customerId,
                'rental-receipt-id': rentalReceiptId,
                'amount': amount
            }),
            headers:{
                'Content-Type': 'application/json'
            }
        }).then(res => res.json())
        .then(data => {
            if(data.code == 200){
                location.reload()
            }
        }).catch(err => console.log(err))
    }
}
