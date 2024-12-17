import hashlib

import cloudinary.uploader
from app import app, db, dao, utils
from flask import render_template, request, redirect, jsonify, url_for
from app.models import UserRole
from flask_login import login_user, logout_user, current_user
import cloudinary
import json




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/reservation')
def reservation():
    return render_template('reservation.html')


@app.route('/login', methods=['post', 'get'])
def login():
    err_mgs = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user_role = request.form.get('user-role')
        try:
            u = dao.check_user(username=username, password=password,
                role=utils.get_user_role(user_role))
            print(u)
            if u:
                login_user(user=u)
                return redirect('/')
            else:
                err_mgs = "username hoặc mật khẩu không đúng!!!"
        except Exception as ex:
            err_mgs = 'Error server' + str(ex)

    return render_template('login.html',
            roles=UserRole,
            err_mgs=err_mgs)

@app.route('/register', methods=['get', 'post'])
def sign_in():
    err_mgs = ''
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        username = request.form.get('username')
        email = request.form.get('email')
        avatar = request.files.get('avatar')
        avatar_path = None
        try:
            if avatar:
                upload_result = cloudinary.uploader.upload(avatar)
                avatar_path = upload_result['secure_url']
                print("sdfsadkfdksf" + avatar_path)
            dao.add_user(password=password, email=email, avatar=avatar_path,
                username=username, role=UserRole.USER)
            return redirect(url_for('login'))
        except Exception as ex:
            err_mgs = "Server error !!!"
            print(str(ex))
            
    return render_template('register.html', err_mgs=err_mgs)

@app.route('/api/check-username', methods=['post'])
def check_username():
    username = request.json.get('username')  
    u = dao.get_user_by_username(username=username)
    if u:
        return jsonify({'code': 201})
    else:
        return jsonify({'code': 200})


@app.route('/sign-out')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/booking', methods=['get', 'post'])
def booking():
    return render_template('booking.html')


# // http://127.0.0.1:5000/booking-detail/1
@app.route('/booking-detail=<int:hotel_id>', methods=['get', 'post'])
def booking_detail(hotel_id=None):
    if hotel_id:
        try:
            # Đọc file JSON dựa vào hotel_id    
            with open(f'app/data/hotel{hotel_id}.json', 'r', encoding='utf-8') as file:
                hotel_data = json.load(file)
        except FileNotFoundError:
            return f"Không tìm thấy dữ liệu cho khách sạn có ID {hotel_id}", 404
    else:
        hotel_data = {}  # Dữ liệu mặc định khi không có hotel_id
    return render_template('bookingDetail.html', hotel=hotel_data)


if __name__ == '__main__':
    app.run(debug=True)

