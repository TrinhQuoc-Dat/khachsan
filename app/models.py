import hashlib
from enum import Enum as EnumRole
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float, DateTime, Boolean
from datetime import datetime
from app import db, app
from sqlalchemy.orm import relationship
from flask_login import UserMixin

class UserRole(EnumRole):
    USER = 1
    ADMIN = 2
    EMPLOYEE = 3


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(255), default="https://res.cloudinary.com/devtqlbho/image/upload/v1734836011/avqqfhy2r_zob90e.webp")
    email = Column(String(50), nullable=False, unique=True)
    created_date = Column(DateTime, default=datetime.now)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    employees = relationship('Employee', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)
    bookings = relationship('Booking', backref='user', lazy=True)

class Employee(db.Model):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(50), nullable=False)
    phone = Column(String(10), nullable=False)
    email = Column(String(50), nullable=False)
    cccd = Column(String(20), nullable=False, unique=True)
    address = Column(String(255))
    salary = Column(Float)
    start_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    rental_receipts = relationship('RentalReceipt', backref='employee', lazy=True)
    bookings = relationship('Booking', backref='employee', lazy=True)


    def __index__(self):
        return self.full_name

class CustomerType(EnumRole):
    DOMESTIC = (1, 1.0) 
    FOREIGN = (2, 1.5)

    def __init__(self, id, multiplier):
        self.id = id
        self.multiplier = multiplier

class Customer(db.Model):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(50), nullable=False)
    phone = Column(String(10))
    email = Column(String(50), nullable=False)
    cccd = Column(String(20), nullable=False, unique=True)
    address = Column(String(255))
    type_customer = Column(Enum(CustomerType), default=CustomerType.DOMESTIC)
    special_info = Column(String(255))

    bookings = relationship('Booking', backref='customer', lazy=True)
    booking_details = relationship('BookingDetail', backref='customer', lazy=True)

    def __index__(self):
        return self.full_name
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'phone': self.phone,
            'email': self.email,
            'cccd': self.cccd,
            'address': self.address,
        }


class OrderType(EnumRole):
    ONLINE = 1
    OFFLINE = 2
    PHONE = 3


class Booking(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    total_customer = Column(Integer, nullable=False)
    total_amount = Column(Float)
    customer_id = Column(Integer, ForeignKey('customer.id', ondelete='CASCADE'), nullable=False)
    order_type_id = Column(Enum(OrderType), default=OrderType.ONLINE)
    employee_id = Column(Integer, ForeignKey(Employee.id, ondelete='SET NULL'))
    booking_details = relationship('BookingDetail', backref='booking', lazy=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

class TypeRoom(EnumRole):
    NORMAL = 1
    VIP = 2

class StatusRoom(EnumRole):
    EMPTY = 1
    BOOK = 2
    RENT = 3
    PROBLEM = 4



class MaxCustomer(EnumRole):
    MOT = (1, 1.0)
    HAI = (2, 1.0)
    BA = (3, 1.25)
    def __init__(self, id, multiplier):
        self.id = id
        self.multiplier = multiplier


class Room(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    max_customer = Column(Enum(MaxCustomer), default=MaxCustomer.HAI)
    price = Column(Float, nullable=False)
    status = Column(Enum(StatusRoom), default=StatusRoom.EMPTY)
    type_room = Column(Enum(TypeRoom), default=TypeRoom.NORMAL)
    image = Column(String(255))
    booking_details = relationship('BookingDetail', backref='room', lazy=True)
    rental_details = relationship('RentalDetail', backref='room', lazy=True)
    comments = relationship('Comment', backref='room', lazy=True)

    def __index__(self):
        return self.name
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "type-room": self.type_room.name,
            "image": self.image
        }

class BookingDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_in = Column(DateTime, default=datetime.now())
    date_out = Column(DateTime, nullable=False)
    discount = Column(Float, default=1)
    room_id = Column(Integer, ForeignKey(Room.id, ondelete='CASCADE'), nullable=False)
    booking_id = Column(Integer, ForeignKey(Booking.id, ondelete='CASCADE'), nullable=False)
    customer_id = Column(Integer, ForeignKey(Customer.id, ondelete='CASCADE'), nullable=False)
    delete = Column(Boolean, default=0)

    def to_id(self):
        return {
            'id': str(id),
            'delete': str(self.delete)
        }


class RentalReceipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    total_customer = Column(Integer)
    note = Column(String(255))
    total_amount = Column(Float)
    employee_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    payments = relationship('Payment', backref='rental_receipt', lazy=True)
    rental_details = relationship('RentalDetail', backref='rental_receipt', lazy=True)


class TypePayment(EnumRole):
    BANKING = 1
    MONEY = 2
    CART = 3


class Payment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    type_payment = Column(Enum(TypePayment), default=TypePayment.MONEY)
    amount = Column(Float, nullable=False)
    status = Column(Boolean, default=False)
    note = Column(String(100))
    rental_receipt_id = Column(Integer, ForeignKey(RentalReceipt.id, ondelete='RESTRICT'), nullable=False)

    def __index__(self):
        return self.id

class RentalDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    number_customer = Column(Integer)
    date_in = Column(DateTime, default=datetime.now)
    date_out = Column(DateTime, default=datetime.now)
    total_amount = Column(Float)
    discount = Column(Float, default=1)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    rental_receipt_id = Column(Integer, ForeignKey(RentalReceipt.id), nullable=False)
    quantity = Column(Integer, default=0)



class Comment(db.Model):
    id = Column(Integer, primary_key= True, autoincrement=True)
    title = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now)
    star = Column(Integer, nullable=False)
    
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        # pass

        db.drop_all()
        db.create_all()
        u = User(username='adminDuy', password=str(hashlib.md5('123'.strip().encode('utf-8')).hexdigest()),
                user_role=UserRole.ADMIN, email='adminDuy@ou.edu.vn')
        u1 = User(username='duy', password=str(hashlib.md5('123'.strip().encode('utf-8')).hexdigest()),
                    user_role=UserRole.USER, email='userduy@ou.edu.vn')
        u2 = User(username='dat', password=str(hashlib.md5('123'.strip().encode('utf-8')).hexdigest()),
                    user_role=UserRole.EMPLOYEE, email='dat@ou.edu.vn')
        db.session.add_all([u1, u2, u])
        db.session.commit()

        
        r1 = Room(name="Phòng Superior Giường Đôi Với Cửa Sổ",
                    max_customer= MaxCustomer.HAI,
                    price=600000,
                    image="https://cf.bstatic.com/xdata/images/hotel/max1024x768/404490378.jpg?k=2a3ee25918786d09794c59ac8b8c67e48414183cf34e9a738d3a8393b09210f5&o=")
        
        r2 = Room(name="Phòng Superior Có Giường Cỡ Queen",
                    max_customer= MaxCustomer.HAI,
                    price=200000,
                    image="https://img.homedy.com/store/images/2020/04/16/phong-ngu-khach-san-5-sao-2-637226034911724690.jpg")
        r3 = Room(name="Phòng Ngủ Tập Thể 6 Giường Cho Cả Nam Và Nữ",
                    max_customer= MaxCustomer.BA,
                    price=800000,
                    image="https://noithatmyhouse.net/wp-content/uploads/2019/06/dien-tich-phong-khach-san-tieu-chuan_2.jpg")
        r4 = Room(name="Phòng gia đình với phòng tắm riêng.",
                    max_customer= MaxCustomer.BA,
                    price=350000,
                    image="https://maximilan.com.vn/wp-content/uploads/2020/03/96515_og_1.jpeg")
        r5 = Room(name="Phòng đơn Superior",
                    max_customer= MaxCustomer.BA,
                    price=200000,
                    image="https://dyf.vn/wp-content/uploads/2021/10/170433841_299853518329337_277745775002707996_n-1.jpg")
        db.session.add_all([r1, r2, r3, r4, r5])
        db.session.commit()

        # db.drop_all()
        # db.create_all()
        # u = User(username='adminDuy', password=str(hashlib.md5('123'.strip().encode('utf-8')).hexdigest()),
        #         user_role=UserRole.ADMIN, email='adminDuy@ou.edu.vn')
        # u1 = User(username='duy', password=str(hashlib.md5('123'.strip().encode('utf-8')).hexdigest()),
        #             user_role=UserRole.USER, email='userduy@ou.edu.vn')
        # u2 = User(username='dat', password=str(hashlib.md5('123'.strip().encode('utf-8')).hexdigest()),
        #             user_role=UserRole.EMPLOYEE, email='dat@ou.edu.vn')
        # db.session.add_all([u1, u2, u])
        # db.session.commit()

        
        # r1 = Room(name="Phòng Superior Giường Đôi Với Cửa Sổ",
        #             max_customer= max_customer.HAI,
        #             price=600000,
        #             image="https://cf.bstatic.com/xdata/images/hotel/max1024x768/404490378.jpg?k=2a3ee25918786d09794c59ac8b8c67e48414183cf34e9a738d3a8393b09210f5&o=")

        # r2 = Room(name="Phòng Superior Có Giường Cỡ Queen",
        #             max_customer= max_customer.BA,
        #             price=200000,
        #             image="https://img.homedy.com/store/images/2020/04/16/phong-ngu-khach-san-5-sao-2-637226034911724690.jpg")
        # r3 = Room(name="Phòng Ngủ Tập Thể 6 Giường Cho Cả Nam Và Nữ",
        #             max_customer= max_customer.BA,
        #             price=800000,
        #             image="https://noithatmyhouse.net/wp-content/uploads/2019/06/dien-tich-phong-khach-san-tieu-chuan_2.jpg")
        # r4 = Room(name="Phòng gia đình với phòng tắm riêng.",
        #             max_customer= max_customer.HAI,
        #             price=350000,
        #             image="https://maximilan.com.vn/wp-content/uploads/2020/03/96515_og_1.jpeg")
        # r5 = Room(name="Phòng đơn Superior",
        #             max_customer= max_customer.BA,
        #             price=200000,
        #             image="https://dyf.vn/wp-content/uploads/2021/10/170433841_299853518329337_277745775002707996_n-1.jpg")

        
       

        
        customer1 = Customer(
        full_name="Nguyễn Văn A",
        phone="0987654321",
        email="nguyenvana@example.com",
        cccd="123456789012",
        address="Hà Nội",
        type_customer=CustomerType.DOMESTIC,
        special_info="Khách hàng thân thiết"
        )

        customer2 = Customer(
            full_name="Trần Thị B",
            phone="0123456789",
            email="tranthib@example.com",
            cccd="987654321098",
            address="Hồ Chí Minh",
            type_customer=CustomerType.FOREIGN,
            special_info="Khách hàng quốc tế"
        )

        db.session.add_all([customer1, customer2])
        db.session.commit()

