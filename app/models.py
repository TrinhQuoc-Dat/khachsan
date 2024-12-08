import hashlib
from enum import Enum as EnumRole
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float, DateTime, Boolean
from datetime import datetime
from app import db, app
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class Person(db.Model):
    __abstract__: True
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(50), nullable=False)
    phone = Column(String(10), nullable=False)
    email = Column(String(50), nullable=False)
    cccd = Column(String(20), nullable=False, unique=True)
    address = Column(String(255))

    def __index__(self):
        return self.full_name

class UserRole(EnumRole):
    USER = 1
    ADMIN = 2
    EMPLOYEE = 3


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(255))
    email = Column(String(50), nullable=False, unique=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    employees = relationship('Employee', backref='user', lazy=True)


class CustomerType(EnumRole):
    DOMESTIC = 1
    FOREIGN = 2


class Customer(db.Model):
    __tablename__ = 'customer'

    person_id = Column(Integer, ForeignKey(Person.id), primary_key=True)
    type_customer = Column(Enum(CustomerType), default=CustomerType.DOMESTIC)
    special_info = Column(String(255))
    bookings = relationship('Booking', backref='customer', lazy=True)
    booking_details = relationship('BookingDetail', backref='customer', lazy=True)
    rental_receipts = relationship('RentalReceipt', backref='customer', lazy=True)
    rental_customers = relationship('RentalCustomer', backref='customer', lazy=True)

    def __index__(self):
        return self.full_name


class Employee(db.Model):
    __tablename__ = 'employee'
    person_id = Column(Integer, ForeignKey(Person.id), primary_key=True)
    salary = Column(Float)
    start_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id))
    rental_receipts = relationship('RentalReceipt', backref='employee', lazy=True)


    def __index__(self):
        return self.full_name

class OrderType(EnumRole):
    ONLINE = 1
    OFFLINE = 2
    PHONE = 3


class Booking(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    total_customer = Column(Integer, nullable=False)
    total_amount = Column(Float)
    customer_id = Column(Integer, ForeignKey(Customer.person_id), nullable=False)
    order_type_id = Column(Enum(OrderType), default=OrderType.ONLINE)
    booking_details = relationship('BookingDetail', backref='booking', lazy=True)


class TypeRoom(EnumRole):
    NORMAL = 1
    VIP = 2

class StatusRoom(EnumRole):
    EMPTY = 1
    BOOK = 2
    RENT = 3
    PROBLEM = 4

class Room(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    max_customer = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(Enum(StatusRoom), default=StatusRoom.EMPTY)
    type_room = Column(Enum(TypeRoom), default=TypeRoom.NORMAL)
    image = Column(String(255))
    booking_details = relationship('BookingDetail', backref='room', lazy=True)

    def __index__(self):
        return self.name

class BookingDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_in = Column(DateTime, default=datetime.now())
    date_out = Column(DateTime, nullable=False)
    discount = Column(Float, default=1)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    booking_id = Column(Integer, ForeignKey(Booking.id), nullable=False)
    customer_id = Column(Integer, ForeignKey(Customer.person_id), nullable=False)


class RentalReceipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    total_customer = Column(Integer)
    note = Column(String(255))
    customer_id = Column(Integer, ForeignKey(Customer.person_id), nullable=False)
    employee_id = Column(Integer, ForeignKey(Employee.person_id), nullable=False)


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
    rental_receipt_id = Column(Integer, ForeignKey(RentalReceipt.id), nullable=False)

    def __index__(self):
        return self.id

class RentalDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    number_customer = Column(Integer)
    date_in = Column(DateTime, default=lambda: datetime.now())
    date_out = Column(DateTime, default=lambda: datetime.now())
    total_amount = Column(Float)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    rental_receipt_id = Column(Integer, ForeignKey(RentalReceipt.id), nullable=False)
    rental_customers = relationship('RentalCustomer', backref='rental_detail', lazy=True)


class RentalCustomer(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    rental_detail_id = Column(Integer, ForeignKey(RentalDetail.id), nullable=False)
    customer_id = Column(Integer, ForeignKey(Customer.person_id), nullable=False)

if __name__ == '__main__':
    with app.app_context():
        pass
        # db.drop_all()
        # db.create_all()
        # u = User(username='Truongdat', password=str(hashlib.md5('123'.strip().encode('utf-8')).hexdigest()),
        #          user_role=UserRole.USER, email='2251050017dat@ou.edu.vn')
        # db.session.add(u)
        # db.session.commit()







