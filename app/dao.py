from app.models import User, UserRole, Room, StatusRoom,BookingDetail, TypeRoom
from app import app, db, login
from sqlalchemy import and_, or_
import hashlib
import json, os

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
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount,
    }
    




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
            avatar = avatar,
            user_role = role,
            email=email)
    db.session.add(u)
    db.session.commit()

    return u

# load dữ liệu khách sạn từ file json 
def load_hotel_data(file_name):
    file_path = os.path.join("data", file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == '__main__':
    with app.app_context():
        u = check_user(username='dat', password=str(123), role=UserRole.USER)
        print(u)

