function checkEmail(input) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(input);
}

function EventCheckMail(e) {
    const errorMgs = document.getElementById('error-message');
    if (e.value == '') return;
    if (!checkEmail(e.value)) {
        errorMgs.innerHTML = 'Mail không tồn tại!!!';
        document.getElementById('error-mail').style.display = 'block';
    } else {
        errorMgs.innerHTML = '';
        document.getElementById('error-mail').style.display = 'none';
    }
}

function EvenCheckUsername(e){
    const errorMgs = document.getElementById('error-message');
    fetch('/api/check-username', {
        method : 'post',
        body: JSON.stringify({
            'username': e.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
    .then(data => {
        if (data.code == 200){
            errorMgs.innerHTML = ''
            document.getElementById('error-mail').style.display = 'none';
            console.log('code' + data.code)
        }
        if (data.code == 201) {
            errorMgs.innerHTML = 'User name đã tồn tại!!!'
            document.getElementById('error-mail').style.display = 'block';
            console.log('code' + data.code)
        }
    }).catch(error => console.error('Error:', error));
}


function EventCheckPassword(e){
    let count = e.value.length
    if (count == 0) return;
    const errorMgs = document.getElementById('error-message');
    if (count < 8) {
        errorMgs.innerHTML = 'Đặt mật khẩu phải lơn hơn 8 ký tự!!!'
        document.getElementById('error-mail').style.display = 'block';
    }else if (count >= 50){
        errorMgs.innerHTML = 'Mật khẩu quá dài!!!'
        document.getElementById('error-mail').style.display = 'block';
    }else{
        errorMgs.innerHTML = ''
        document.getElementById('error-mail').style.display = 'none';
    }
}

function EventCheckConfirm(e){
    let password = document.getElementById('password').value
    const errorMgs = document.getElementById('error-message');
    if (password){
        confir = e.value
        if(password === confir){
            errorMgs.innerHTML = ''
            document.getElementById('error-mail').style.display = 'none';
        }else {
            errorMgs.innerHTML = 'Nhập lại mật khẩu không chính xác!!!'
            document.getElementById('error-mail').style.display = 'block';
        }
    }else{
        errorMgs.innerHTML = 'Vui lòng nhập Mật khẩu!!!'
        document.getElementById('error-mail').style.display = 'block';
    }
}





