
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

class AuthenticatedView(BaseView):
      def is_accessible(self):
            return current_user.is_authenticated

class LogoutView(AuthenticatedView):
      @expose('/')
      def index(self):
            logout_user()
            return redirect('/admin')

# class StatisticView(AuthenticatedView):
#       @expose('/')
#       def index(self):
#             return self.render('/admin/statistics.html')
class StatisticView(AuthenticatedView):
      @expose('/')
      def index(self):
            tong_doanh_thu = 8000000000  
            so_phong_su_dung = 120 
            doanh_thu = [1000000, 1500000, 2000000, 2500000, 3000000, 3500000, 4000000, 4500000, 5000000, 5500000, 6000000, 6500000]
            tan_suat = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140]
            return self.render('/admin/statistics.html', tong_doanh_thu=tong_doanh_thu, so_phong_su_dung=so_phong_su_dung, doanh_thu=doanh_thu, tan_suat=tan_suat)     

# ghi trước, chưa có dữ liệu thực
class statis_doanh_thu(AuthenticatedView):
      @expose('/')
      def index(self):
            return self.render('/admin/thong_ke_doanh_thu.html')

class MyAdminIndex(AdminIndexView):
      @expose('/')
      def __index__(self):
            return self.render('/admin/index.html')


class UserView (AuthenticatecModelView):
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
admin.add_view(StatisticView(name='Thống Kê', endpoint='thong_ke', category="Thống kê"))
admin.add_view(StatisticView(name='Báo cáo Doanh Thu', endpoint='bao_cao_doanh_thu', category="Thống kê"))
admin.add_view(StatisticView(name='Mật Độ Sử Dụng Phòng', endpoint='mat_do_su_dung_phong', category="Thống kê"))


