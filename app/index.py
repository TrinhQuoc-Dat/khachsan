import hashlib
import math
import cloudinary.uploader
from app import app, db, dao, utils
from flask import render_template, request, redirect, jsonify, url_for, session
from app.models import UserRole, StatusBooking, CustomerType
from flask_login import login_user, logout_user, current_user, login_required
import cloudinary
import json
from app import login
from datetime import datetime, timedelta, date
from app.models import User, Customer, UserRole, Employee, Booking, Room,StatusRoom, BookingDetail, RentalReceipt, Payment, RentalDetail
from sqlalchemy import func,and_

@app.route('/')
def home():
    with open(f'app/data/home.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return render_template('index.html', data = data)

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

        customer = dao.search_customer(cccd)
        cart = session.get('cart')

        if cart:
            stast = dao.count_cart(cart)
            if customer is None:
                customer = dao.add_customer(name=name, email=email, cccd=cccd, phone=phone )
            booking = dao.add_booking(total_amount=stast['total_amount'],
                                    total_customer=utils.count_customer(cart=cart),
                                    customer = customer)
            for r in cart.values():
                cm = request.form.get('cccd' + r['id'])
                c = dao.search_customer(cm)
                if c is None:
                    c = dao.add_customer(name=request.form.get('name' + r['id']), 
                                        email=request.form.get('email' + r['id']), 
                                        cccd=cm,
                                        address=request.form.get('address' + r['id']),
                                        type_customer=request.form.get('type-customer' + r['id']))
                if c.address is None:
                    c.address = request.form.get('address' + r['id'])
                    db.session.add(c)
                    db.session.commit()
                bd = dao.add_bookingdetail(room_id=r['id'],
                                            date_in=r['date_in'],
                                            date_out=r['date_out'],
                                            booking = booking,
                                            customer = c,
                                            discount = 0.9)
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
        if c:
            return jsonify({'code': 200, 'customer': c })
        else:
            return jsonify({'code': 400})
    except Exception as ex:
        return jsonify({'code ': 500, 'error': str(ex)})
    
@app.route('/api/lap-phieu-thue-phong', methods=['post'])
@login_required
def rental_room():
    if request.method.__eq__('POST'):
        try:
            booking_id = request.json.get('booking_id')
            customer_id = request.json.get('customer-id')
            rooms = request.json.get('rooms', [])
            booking = dao.get_booking_id(booking_id=booking_id)
            books = dao.get_booking_rental(booking_id)
            employee = dao.get_employee(current_user.id)
            rental = dao.add_rental_receipt(employee_id=employee, customer_id= customer_id)
            total = 0
            for book in books:
                number_customer = next(
                    (room['number_customer'] for room in rooms if room['room_id'] == str(book[0])), 1)
                
                days = (book[4] - book[3]).days
                total += book[1] * book[5] * days
                dao.add_rental_detail(
                    date_in=book[3],
                    date_out=book[4],
                    number_customer=number_customer,
                    total_amount=book[1] * book[5] * days,
                    room_id=book[0],
                    rental_receipt_id=rental,
                    customer_id=book[6]
                )
            rental.total_amount = total
            booking.status = StatusBooking.RENTAL
            db.session.commit()
            return jsonify({'code': 200})
        except Exception as ex:
            print("Error occurred:", ex)
            return jsonify({'code': 500, 'error': 'Lỗi Server!!!'})

@app.route('/api/search-rental', methods=['post'])
def search_rental():
    try:
        name = request.json.get('name')
        rental = dao.get_rental_payment(name)
        rental_dict = {}
        if rental:
            for rental_detail, customer, room, rental_receipt in rental:
                receipt_id = rental_receipt.id
                if receipt_id not in rental_dict:
                    rental_dict[receipt_id] = {
                        'rental_receipt': rental_receipt.to_dict(),
                        'details' : []
                    }

                rental_dict[receipt_id]['details'].append({
                    'customer': customer.to_dict(),
                    'room': room.to_dict(),
                    'receipt_detail': rental_detail.to_dict()
                })
            return jsonify({'code': 200, 'rental': rental_dict})
        else:
            return jsonify({'code': 400, 'error': 'Không tìm thấy phiếu Thuê phòng!!!'})
    except Exception as ex:
        return jsonify({'code': 500, 'error': "Lỗi server!!!"})

@app.route('/api/payment', methods=['post'])
def payment():
    if request.method.__eq__('POST'):
        try:
            rr_id = request.json.get('rental-receipt-id')
            c_id = request.json.get('customer-id')
            amount = request.json.get('amount')

            pay = dao.add_payment(rental_id = rr_id,
                                customer_id = c_id,
                                amount = amount)
            if pay:
                return jsonify({'code': 200})
        except Exception as ex:
            return jsonify({'code': 500, 'error': "Lỗi Server!!!"})

@app.route('/api/search-room-rental', methods=['post'])
@login_required
def search_room_rental():
    if request.method.__eq__("POST"):
        type = request.json.get('type')
        date_in = request.json.get('date-in')
        date_out = request.json.get('date-out')

        print(type, date_in, date_out)
        try:

            rooms = dao.get_room_search(type_room=type, date_in=date_in, date_out=date_out)
            if rooms:
                rooms = [room.to_dict() for room in rooms]
                return jsonify({'code': 200, 'rooms': rooms})
            else:
                return jsonify({'code': 400, 'mess': 'Hết phòng!!!'})
        except Exception as ex:
            return jsonify({'code': 500, 'mess': 'Lỗi server!!!'})

@app.route('/api/add-rental-receipt', methods=['post'])
@login_required
def add_rental_receipts():
    if request.method.__eq__('POST'):
        try:
            data = request.json.get('data')
            receipt = None
            for d in data:
                customer = d['customer']
                room = d['room']
                print(room['check_in_date'])
                c = dao.search_customer(customer['cccd'])
                if c is None:
                    type = None
                    if customer['typeCustomer'] == 'DOMESTIC':
                        type = CustomerType.DOMESTIC
                    else:
                        type = CustomerType.FOREIGN
                    c = dao.add_customer(name=customer['name'],
                                         email=customer['email'],
                                         cccd=customer['cccd'],
                                         phone=customer['phone'],
                                         type_customer=type)
                print(c)
                
                employee = dao.get_employee(current_user.id)
                print(employee)
                if receipt is None:
                    tong = 0
                    for d in data:
                        tong += d['room']['total_amount']
                    receipt = dao.add_rental_receipt(employee_id=employee,
                                                 customer_id=c.id, total_amount = tong)
                print(receipt)
                r_detail = dao.add_rental_detail(date_in=datetime.fromisoformat(room['check_in_date'].replace("Z", "")).date(),
                                    date_out=datetime.fromisoformat(room['check_out_date'].replace("Z", "")).date(),
                                    total_amount=room['total_amount'],
                                    number_customer=room['number_customer'],
                                    room_id=room['room_id'],
                                    rental_receipt_id = receipt,
                                    customer_id = c.id)
                print(r_detail)

            return jsonify({'code': 200})
        except Exception as ex:
            return jsonify({'code': 500, 'mess': 'Lỗi server!!!'})

@app.route('/login', methods=['post', 'get'])
def login():
    err_mgs = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user_role = dao.get_user_role(request.form.get('user-role'))
        
        try:
            u = dao.check_user(username=username, password=password,
                role=user_role)
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

@app.route('/api/overview', methods=['GET']) 
def overView():
    stats = dao.revenue_by_month()
    data = [{'month': int(s[0]), 'revenue': float(s[1])} for s in stats]
    return jsonify(data)

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

@app.route('/api/comment', methods=['POST'])
@login_required
def add_comment():
    data = request.json
    title = data.get('title')
    comment = data.get('comment')
    room_id = data.get('room_id')
    star = data.get('star')
    
    try:
        c = dao.add_comment(star=star,
                            comment = comment, 
                            room_id = room_id, 
                            title=title)
        return jsonify({'status': 201, 'comment': {
            'id': c.id,
            'title': c.title,
            'comment': c.comment,
            'created_date': c.created_date,
            'star': c.star,
            'avatar': current_user.avatar,
            'name': current_user.username
        }})
    except:
        return jsonify({'status': 404, 'err_msg': "lỗi"})


@app.route('/booking-detail/<int:hotel_id>', methods=['get', 'post'])
def booking_detail(hotel_id):
    room = None
    if hotel_id:
        try:
            comment = dao.get_comment(hotel_id)
            room = dao.get_room_id(hotel_id)
            with open(f'app/data/hotel1.json', 'r', encoding='utf-8') as file:
                hotel_data = json.load(file)
                print(comment)
        except Exception as ex:
            return f"Không tìm thấy phòng có ID là {{ hotel_id }}" + hotel_id
    else:
        hotel_data = {} 
    return render_template('bookingDetail.html', hotel=hotel_data, 
                           room=room, comment=comment)

if __name__ == '__main__':
    from app.admin import *
    app.run(debug=True)

