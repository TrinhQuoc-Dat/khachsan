import hashlib
import math
import cloudinary.uploader
from app import app, db, dao, utils
from flask import render_template, request, redirect, jsonify, url_for, session
from app.models import UserRole
from flask_login import login_user, logout_user, current_user
import cloudinary
import json
from app import login
from datetime import datetime, timedelta, date


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/reservation')
def reservation():
    return render_template('reservation.html')


@app.route('/login-admin', methods=['post'])
def singin_admin():
    username = request.form.get("username")
    password = request.form.get("password")
    user = dao.check_user(username=username,
                        password=password,
                        role=UserRole.ADMIN)
    if user:
        login_user(user=user)
    return redirect('/admin')

@app.route('/api/booking/search-room', methods=['post'])
def search_room():
    name = request.json.get('nameRoom')
    date_in = request.json.get('dateIn')
    date_out = request.json.get('dateOut')
    type_room = request.json.get('typeRoom')

    date_out = datetime.strptime(date_out, "%Y-%m-%dT%H:%M:%S.%fZ")

    print(name, date_out, date_in, type_room)

    try:
         rooms = dao.get_room_search(name_room=name,
                                date_in=date_in,
                                date_out=date_out,
                                type_room=type_room)
    
         rooms = [room.to_dict() for room in rooms]
         print(rooms)
         if rooms:
             return jsonify({'code': 200, 'rooms': rooms})
         else:
             return jsonify({'code': 404, 'error': 'No rooms found'})
    except Exception as ex:
        return jsonify({
            'code': 500, 
            'error' : str(ex)
        })


@app.route('/api/add-room-cart', methods=['post'])
def add_room_cart():
    id = request.json.get('id')
    name = request.json.get('nameRoom')
    price = request.json.get('price')
    type_room = request.json.get('type-room')
    image = request.json.get('image')

    cart = session.get('cart')

    if not cart:
        cart = {}

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'type_room': type_room,
            'image': image,
            'quantity': 1
        }

    session['cart'] = cart
    return jsonify(dao.count_cart(cart))



@app.route('/login', methods=['post', 'get'])
def login():
    err_mgs = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user_role = utils.get_user_role(request.form.get('user-role'))
        
        try:
            u = dao.check_user(username=username, password=password,
                role=user_role)
            print(u)
            if u:
                login_user(user=u)
                if (user_role == UserRole.ADMIN):
                    return redirect('/admin')
                else:
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



@app.context_processor
def common_response():
    return {
        "cart_stats": dao.count_cart(session.get('cart'))

    }


@app.route('/sign-out')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/booking', methods=['get', 'post'])
def booking():
    page = int(request.args.get('page', 1))
    counter = dao.count_room()
    end = math.ceil(counter/app.config['PAGE_SIZE'])
    has_prev = page > 1
    has_next = page < end

    return render_template('booking.html', 
                           rooms = dao.get_rooms(page=page), 
                           pages=end,
                           page=page,
                           has_next=has_next,
                           has_prev=has_prev)


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
    from app.admin import *
    app.run(debug=True)

