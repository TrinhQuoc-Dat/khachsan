import hashlib
import math
import cloudinary.uploader
from app import app, db, dao, utils
from flask import render_template, request, redirect, jsonify, url_for, session
from app.models import UserRole
from flask_login import login_user, logout_user, current_user, login_required
import cloudinary
import json
from app import login
from datetime import datetime, timedelta, date
from app.models import User, Customer, UserRole, Employee, Booking, Room,StatusRoom, BookingDetail, RentalReceipt, Payment, RentalDetail
from sqlalchemy import func,and_
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cart')
@login_required
def cart():
    return render_template('cart.html')

@app.route('/reservation', methods=['post', 'get'])
@login_required
def reservation():
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        cccd = request.form.get('cccd')
        email = request.form.get('email')
        phone = request.form.get('phone')

        cart = session.get('cart')
       
        if cart:
            stast = dao.count_cart(cart)
            customer = dao.add_customer(name=name, email=email, cccd=cccd, phone=phone )
            booking = dao.add_booking(total_amount=stast['total_amount'],
                                    total_customer=utils.count_customer(cart=cart),
                                    customer = customer)
            for r in cart.values():
                c = dao.add_customer(name=request.form.get('name' + r['id']), 
                                    email=request.form.get('email' + r['id']), 
                                    cccd=request.form.get('cccd' + r['id']),
                                    address=request.form.get('address' + r['id']),
                                    type_customer=request.form.get('type-customer' + r['id']))
                bd = dao.add_bookingdetail(room_id=r['id'],
                                           date_in=r['date_in'],
                                           date_out=r['date_out'],
                                           booking = booking,
                                           customer = c)
            session.pop('cart', None)
            return redirect('/reservation')
    
    booking = dao.get_booking(current_user.id)
    print(booking)
    return render_template('reservation.html', booking=booking)


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

    if date_out:
        date_out = datetime.strptime(date_out, "%d/%m/%Y")

    date_obj = datetime.strptime(date_in, '%d/%m/%Y')
    date_in = date_obj.strftime('%Y-%m-%d')

    try:
         rooms = dao.get_room_search(name_room=name,
                                date_in=date_in,
                                date_out=date_out,
                                type_room=type_room)
    
         rooms = [room.to_dict() for room in rooms]
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
@login_required
def add_room_cart():
    id = request.json.get('id')
    name = request.json.get('name')
    price = request.json.get('price')
    type_room = request.json.get('type-room')
    image = request.json.get('image')
    date_in = request.json.get('date-in')
    date_out = request.json.get('date-out')
    day = request.json.get('day')
    number_customer = request.json.get('number-customer')

    date_obj = datetime.strptime(date_out, '%d/%m/%Y')
    date_out = date_obj.strftime('%Y-%m-%d')

    cart = session.get('cart')

    if not cart:
        cart = {}

    if id in cart:
        return jsonify({'code': 301, 'mess': 'Không thể thêm phòng vì đã có trong giỏ đặt phòng!!!'})
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'type_room': type_room,
            'image': image,
            'number_customer': number_customer ,
            'date_in': date_in,
            'date_out': date_out,
            'day': day,
        }
    # session.pop('cart', None)
    session['cart'] = cart
    return jsonify({'code': 300, 'mess': dao.count_cart(cart)})


@app.route('/api/delete-room', methods=["post"])
def delete_room_cart():
    id = request.json.get('id')
    cart = session.get('cart')
    if cart and id in cart:
        del cart[id]
        session['cart'] = cart
        print(cart)
    return jsonify({'mess': dao.count_cart(cart)})


@app.route('/api/delete-booking-detail/<int:id>', methods=['delete'])
@login_required
def delete_booking_detail(id):
    book = dao.delete_booking_detail(id)
    if book:
        return jsonify({'code': 200, 'booking_detail': book.to_id()})
    else:
        return jsonify({'code ': 500, 'error': "Lỗi server!!!"})
    
@app.route('/api/search-customer', methods=['post'])
@login_required
def search_customer():
    id = request.json.get('id')

    try:
        c = dao.search_customer(id)
        c = c.to_dict() if c else None
        print(c)
        if c:
            return jsonify({'code': 200, 'customer': c })
        else:
            return jsonify({'code': 400})
    except Exception as ex:
        return jsonify({'code ': 500, 'error': str(ex)})
    


@app.route('/api/lap-phieu-thue-phong', methods=['post'])
@login_required
def rental_room():
    booking_id = request.json.get('bookind_id')

    e_id = current_user.id

    rd = dao.add_rental_receipt(e_id)
    rental = dao.get_booking_rental(booking_id)

    print(rental)

    return jsonify({'code' : 200})



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

@app.route('/api/revenue', methods=['POST'])
def revenueStats_by_time():
    data = request.get_json()
    stats = dao.revenue_stats_Room(month=data.get('month'), year=data.get('year'))
    return jsonify({
        "normal": stats[0],
        "vip": stats[1]
    })

@app.route('/api/frequency', methods=['POST'])
def frequency_by_time():
    # Lấy dữ liệu từ request
    data = request.get_json()

    month = data.get('month', datetime.now().month)  # Nếu không có tháng, sử dụng tháng hiện tại
    year = data.get('year', datetime.now().year)  # Nếu không có năm, sử dụng năm hiện tại

    # Gọi hàm thống kê
    stats = dao.frequency_stats_Room(month=month, year=year)

    result = [
        {
            'stt': index + 1,
            'room_id': row["room_id"],
            'room_name': row["room_name"],
            'days_rented': row["days_rented"],
            'usage_rate': row["usage_rate"]
        }
        for index, row in enumerate(stats)
    ]
    return jsonify(result)

@app.route('/admin/frequencyStats', methods=['GET'])
def frequencyStats():
    return render_template('admin/frequencyStats.html')

@app.context_processor
def common_response():
    return {
        "cart_stats": dao.count_cart(session.get('cart'))
    }

@app.route('/api/overview', methods=['GET', 'POST'])
def get_overview():
    try:
        
        today = datetime.now().date()
        current_month = today.month
        current_year = today.year
        # Số phòng trống
        empty_rooms = Room.query.filter_by(status=StatusRoom.EMPTY).count()
        # Số phòng đã đặt
        booked_rooms = Room.query.filter_by(status=StatusRoom.BOOK).count()
        # Số khách hiện tại đang ở
        current_guests = db.session.query(func.count(RentalDetail.id)).filter(
            and_(
                RentalDetail.date_in <= datetime.now(),
                RentalDetail.date_out >= datetime.now(),
            )
        ).scalar() or 0
        
        booking_today = Booking.query.filter(func.date(Booking.created_date.__eq__(today))).count()
    
        current_month_revenue = db.session.query(func.sum(Payment.amount)).filter(
            and_(
                func.extract('month', Payment.created_date) == current_month,
                func.extract('year', Payment.created_date) == current_year
            )
        ).scalar() or 0
        
        return jsonify({
            'empty_rooms': empty_rooms,
            'booked_rooms': booked_rooms,
            'current_guests': current_guests,
            'booking_today': booking_today,
            'month_revenue': float(current_month_revenue)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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


# // http://127.0.0.1:5000/booking-detail=1
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
        hotel_data = {} 
    return render_template('bookingDetail.html', hotel=hotel_data)


if __name__ == '__main__':
    from app.admin import *
    app.run(debug=True)

