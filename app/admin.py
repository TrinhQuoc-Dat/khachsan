
from flask_admin import Admin, BaseView, AdminIndexView, expose
from app import app, db
from app.models import User, Person, Customer, UserRole, Employee, Booking, Room, BookingDetail, RentalReceipt, Payment, RentalDetail, RentalCustomer
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect, render_template, request
from datetime import datetime
from app import dao



class AuthenticatecModelView(ModelView):
      def is_accessible(self):
            return (current_user.is_authenticated and
                  current_user.user_role.__eq__(UserRole.ADMIN))

class LogoutView(BaseView):
      @expose()
      def __index__(self):
            logout_user()
            return redirect('/admin')

      def is_accessible(self):
            return current_user.is_authenticated

class MyAdminIndex(AdminIndexView):
      @expose('/')
      def __index__(self):
            return self.render('/admin/index.html')


class UserView (ModelView):
      column_display_pk = True
      column_searchable_list = ['username', 'email']
      column_filters = ['username', 'email']
      column_editable_list = ['username', 'email', 'password']
      column_exclude_list = ['password']
      form_excluded_columns = ['password']
      form_widget_args = {
            'password': {
                  'type': 'password'
            }
      }
      can_export = True
      page_size = 10

class RoomView(AuthenticatecModelView):
      column_display_pk = True
      column_searchable_list = [ 'name', 'price','max_customer', 'type_room']
      column_filters = ['name', 'price','max_customer','status', 'type_room','booking_details']
      column_editable_list = ['name', 'max_customer','price','status', 'type_room',  "image"]
      can_export = True
      page_size = 10
      
class PersonView (AuthenticatecModelView):
      column_display_pk = True
      column_searchable_list = ['full_name', 'phone', 'email']
      column_filters = ['full_name', 'phone', 'email', 'cccd', 'address']
      column_editable_list = ['full_name', 'phone', 'email']
      can_export = True
      page_size = 10




admin = Admin(app=app,
            name="Hotel Management", 
            template_mode='bootstrap4',
            index_view=MyAdminIndex())


# Tổ chức các danh mục
admin.add_view(UserView(User, db.session, category="Quản lý người dùng"))
admin.add_view(PersonView(Person, db.session, category="Quản lý người dùng"))
admin.add_view(AuthenticatecModelView(Customer, db.session, category="Quản lý người dùng"))
admin.add_view(AuthenticatecModelView(Employee, db.session, category="Quản lý người dùng"))

admin.add_view(RoomView(Room, db.session, category="Quản lý phòng"))

admin.add_view(AuthenticatecModelView(Booking, db.session, category="Quản lý đặt phòng"))
admin.add_view(AuthenticatecModelView(BookingDetail, db.session, category="Quản lý đặt phòng"))

admin.add_view(AuthenticatecModelView(RentalReceipt, db.session, category="Quản lý hóa đơn"))
admin.add_view(AuthenticatecModelView(Payment, db.session, category="Quản lý hóa đơn"))

admin.add_view(AuthenticatecModelView(RentalDetail, db.session, category="Quản lý thuê phòng"))
admin.add_view(AuthenticatecModelView(RentalCustomer, db.session, category="Quản lý thuê phòng"))

admin.add_view(LogoutView(name='Logout'))


