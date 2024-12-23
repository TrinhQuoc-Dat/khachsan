from app.models import User, UserRole, Room, StatusRoom,BookingDetail, TypeRoom, Customer, CustomerType, OrderType, Booking, RentalDetail
from app.models import RentalCustomer
from sqlalchemy import and_, or_, func
from app import app, db, login
import hashlib
import json, os
import cloudinary.uploader
from flask_login import current_user

def check_user(username, password, role=UserRole.USER):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()),
                            User.password.__eq__(password),
                            User.user_role.__eq__(role)).first()
    
@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


def get_user_by_username(username):
    return User.query.filter(User.username.__eq__(username)).first()

def get_room_search(name_room=None, date_in=None, date_out=None, type_room=None):
    room = Room.query.filter(Room.status.__eq__(StatusRoom.EMPTY))

    page_size = app.config['PAGE_SIZE']

    if name_room:
        room = room.filter(Room.name.contains(name_room))
    
    if type_room == 'Normal':
        room = room.filter(Room.type_room.__eq__(TypeRoom.NORMAL))
    else:
        room = room.filter(Room.type_room.__eq__(TypeRoom.VIP))

    
    if date_in and date_out:
        room = room.filter(
            ~Room.id.in_(
                db.session.query(BookingDetail.room_id).filter(
                    or_(
                        and_(BookingDetail.date_in <= date_in, BookingDetail.date_out > date_in),
                        and_(BookingDetail.date_in < date_out, BookingDetail.date_out >= date_out),
                        and_(BookingDetail.date_in >= date_in, BookingDetail.date_out <= date_out)
                    )
                )
            ))
    
    return room.all()


def count_cart(cart):
    total_quantity, total_amount = 0, 0

    if cart: 
        for c in cart.values():
            total_quantity += 1
            total_amount += c['price'] * int(c['day'])

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount,
    }
    

def add_customer(name, email, cccd, phone = None, address=None , type_customer = CustomerType.DOMESTIC, **kwa):
    c = Customer(full_name=name,
                    email= email,
                    cccd = cccd,
                    phone = phone,
                    address = address,
                    type_customer = type_customer)
    
    db.session.add(c)
    db.session.commit()
    return c


def add_booking(total_amount, total_customer, customer, employee_id = None, order_type_id = OrderType.ONLINE ):
    b = Booking(total_customer = total_customer,
                customer = customer,
                total_amount = total_amount,
                order_type_id = order_type_id,
                employee_id = employee_id,
                user = current_user)
    db.session.add(b)
    db.session.commit()
    return b


def get_booking(user_id):
    b = db.session.query(Room.id, Room.name, Room.image, 
                            Booking.created_date, Booking.total_amount, BookingDetail.date_in, 
                            BookingDetail.date_out, Booking.id, func.sum(Room.price * func.datediff(BookingDetail.date_out, BookingDetail.date_in) * BookingDetail.discount), BookingDetail.id,BookingDetail.delete)\
                            .join(Room, BookingDetail.room_id.__eq__(Room.id))\
                            .join(Booking, BookingDetail.booking_id.__eq__(Booking.id))\
                            .filter(Booking.user_id.__eq__(user_id))\
                            .group_by(Room.id, Room.name, Room.image, 
                            Booking.created_date, Booking.total_amount, BookingDetail.date_in, 
                            BookingDetail.date_out, Booking.id, BookingDetail.id, BookingDetail.delete)\
                            .order_by(-BookingDetail.id)
    return b.all()

def get_booking_name(name):
    b = db.session.query(Room.id, Room.name, Booking.id, Booking.created_date, Booking.total_amount, 
                          BookingDetail.id, BookingDetail.date_in, BookingDetail.date_out, Customer.id, Customer.full_name)\
                          .join(Room, BookingDetail.room_id.__eq__(Room.id))\
                          .join(Booking, BookingDetail.booking_id.__eq__(Booking.id))\
                          .join(Customer, Booking.customer_id.__eq__(Customer.id))\
                          .filter(Customer.full_name.contains(name), BookingDetail.delete.__eq__(0))
    return b.all()


# def get_name_booking(name):
#     b = db.session.query(Booking.id, Booking.created_date, Booking.total_amount, Customer.id, Customer.full_name)\
#                         .join(Customer, Booking.customer_id.__eq__(Customer.id))\
#                         .filter(Customer.full_name.contains(name))
#     return b.all()


def get_booking_detail(id):
    return BookingDetail.query.get(id)


def delete_booking_detail(id):
    book = get_booking_detail(id)

    book.delete = True
    db.session.commit()
    return book


def add_bookingdetail(date_in, date_out, room_id, booking, customer, discount = 1):
    bd = BookingDetail(date_in = date_in,
                    date_out = date_out,
                    discount = discount,
                    room_id= room_id,
                    booking = booking,
                    customer = customer)
    db.session.add(bd)
    db.session.commit()
    return bd

def get_rooms(page):
    room = Room.query.filter(Room.status.__eq__(StatusRoom.EMPTY))
    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    return room.slice(start=start, stop=end).all()

def count_room(name_room=None, date_in=None, date_out=None, type_room=None):
    query = db.session.query(Room)

    if name_room:
        query = query.filter(Room.name.ilike(f"%{name_room}%"))
    if date_in and date_out:
        query = query.filter(
            ~Room.id.in_(
                db.session.query(BookingDetail.room_id).filter(
                    or_(
                        and_(BookingDetail.date_in <= date_in, BookingDetail.date_out > date_in),
                        and_(BookingDetail.date_in < date_out, BookingDetail.date_out >= date_out),
                        and_(BookingDetail.date_in >= date_in, BookingDetail.date_out <= date_out),
                    )
                )
            )
        )
    if type_room:
        query = query.filter(Room.type_room == type_room)

    return query.count()


def add_user(username, password, avatar, role, email):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(username = username,
            password = password,
            user_role = role,
            email=email)
    
    if avatar:
        res = cloudinary.uploader.upload(avatar)
        u.avatar = res.get('secure_url')
    
    db.session.add(u)
    db.session.commit()
    return u

# load dữ liệu khách sạn từ file json 
def load_hotel_data(file_name):
    file_path = os.path.join("data", file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def revenue_stats_Room():
    return db.session.query(Room.id, Room.name, func.sum(RentalDetail.quantity * Room.price * RentalDetail.discount * Customer.type_customer * Room.max_customer))\
            .join(RentalDetail, RentalDetail.room_id.__eq__(Room.id)).join(RentalCustomer, RentalCustomer.rental_detail_id.__eq__(RentalDetail.id))\
            .join(Customer, Customer.id.__eq__(RentalCustomer.customer_id)).group_by(Room.id,Room.name,Room.type_room).all()

if __name__ == '__main__':
    with app.app_context():
        # u = check_user(username='dat', password=str(123), role=UserRole.USER)
        # print(u)
        # b = get_booking()
        # print(b)
        print(revenue_stats_Room())

