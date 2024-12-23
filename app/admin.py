from flask_admin import Admin, BaseView, AdminIndexView, expose
from app import app, db
from app.models import User, Customer, UserRole, Employee, Booking, Room, BookingDetail, RentalReceipt, Payment, RentalDetail
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect, render_template, request
from datetime import datetime
from app import dao, utils
from wtforms.validators import NumberRange
from collections import defaultdict

from flask_admin.contrib.sqla import ModelView
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_wtf import FlaskForm
from wtforms import SubmitField
from cloudinary.uploader import upload

class AuthenticatecModelView(ModelView):
      def is_accessible(self):
            return (current_user.is_authenticated and
                  current_user.user_role.__eq__(UserRole.ADMIN))

class AuthenticatedView(BaseView):
      def is_accessible(self):
            return (current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN))
      

      

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


class PaymentConfirmation(BaseView):
      @expose('/')
      def index(self):
            return self.render('/admin/payment.html')
      
      def is_accessible(self):
            return (current_user.is_authenticated and
                  current_user.user_role.__eq__(UserRole.EMPLOYEE))


class RentalRoom(BaseView):
    @expose('/')
    def index(self, **kwargs):
            name = request.args.get('name')
            bookings = None
            grouped_data = defaultdict(lambda: {
                  'customer_id': None,
                  'customer_name': None,
                  'booking_id': None,
                  'booking_date': None,
                  'booking': {}
            })

            if name:
                  bookings = dao.get_booking_name(name=name)
                  for booking in bookings:
                        room_id = booking[0]
                        room_name = booking[1]
                        booking_id = booking[2]
                        booking_date = booking[3]
                        total_amount = booking[4]
                        booking_detail_id = booking[5]
                        check_in_date = booking[6]
                        check_out_date = booking[7]
                        customer_id = booking[8]
                        customer_name = booking[9]

                        if not grouped_data[customer_id]['customer_id']:
                              grouped_data[customer_id]['customer_id'] = customer_id
                              grouped_data[customer_id]['customer_name'] = customer_name
                              grouped_data[customer_id]['booking_id'] = booking_id
                              grouped_data[customer_id]['booking_date'] = booking_date

                        grouped_data[customer_id]['booking'][room_id] = {
                              'room_id': room_id,
                              'room_name': room_name,
                              'booking_detail_id': booking_detail_id,
                              'check_in_date': check_in_date,
                              'check_out_date': check_out_date,
                              'total_amount': total_amount
                        }

            return self.render('/admin/RentalRoom.html', bookings=grouped_data)

    def is_accessible(self):
        return (current_user.is_authenticated and
                current_user.user_role.__eq__(UserRole.EMPLOYEE))

class MyAdminIndex(AdminIndexView):
      @expose('/')
      def __index__(self):
            return self.render('/admin/index.html')



class UserView(AuthenticatecModelView):
      column_display_pk = True
      form_column = ['id', 'username', 'email', 'avatar', 'password', 'user_role']
      column_searchable_list = ['username', 'email', 'user_role']
      column_filters = ['username', 'email', 'user_role']
      column_editable_list = [ 'username', 'email', 'avatar', 'password', 'user_role']
      column_exclude_list = ['password']
      # form_excluded_columns = ['password']
      
      column_labels = {
            'id': 'ID',
            'username': 'Tên người dùng',
            'email': 'Email',
            'avatar': 'Ảnh đại diện',
            'password': 'Mật khẩu',
            'user_role': 'Vai trò',
}
      form_widget_args = {
            'password': {
                  'type': 'password'
            }
      }
      can_export = True
      page_size = 10
      form_extra_fields = {
            'avatar': FileField(
                  'Avatar',
                  validators=[
                  FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Only image files are allowed!')
                  ]
            )
      }
      
      def on_model_change(self, form, model, is_created):
            avatar = form.avatar.data  
            if avatar:
                  upload_result = upload(avatar, folder="avatars")
                  model.avatar = upload_result.get("secure_url")
            super().on_model_change(form, model, is_created)


      def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class RoomView(AuthenticatecModelView):
      column_display_pk = True
      column_searchable_list = [ 'name', 'price','max_customer', 'type_room']
      column_filters = ['name', 'price','max_customer','status', 'type_room','booking_details']
      column_editable_list = ['name', 'max_customer','price','status', 'type_room',  "image"]
      can_export = True
      page_size = 10
      

      form_choices = {
            'max_customer': [
                  (1, '1'),
                  (2, '2'),
                  (3, '3')
            ]
      }
      column_formatters = {
            'price': lambda v, c, m, p: f"{m.price:,.1f}"
      }
      form_extra_fields = {
            'image': FileField(
                  'image',
                  validators=[
                  FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Only image files are allowed!')
                  ]
            )
      }
      column_labels = {
            'id': 'mã phòng',
            'name': 'Tên Phòng',
            'max_customer': 'Số khách tối đa',
            'price': 'Giá phòng',
            'status':'Tình trạng phòng',
            'type_room':'Loại phòng',
            'image': 'Hình ảnh',
      }
      def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class customerView(AuthenticatecModelView):
      column_display_pk = True
      column_searchable_list = ['full_name', 'phone', 'email',  'cccd']
      column_filters = ['full_name', 'phone', 'email', 'cccd', 'address']
      column_editable_list = ['full_name', 'phone', 'email']
      can_export = True
      page_size = 10
      column_labels = {
            'id': 'ID',
            'full_name': 'Tên khách hàng',
            'phone': 'Số điện thoại',
            'cccd': 'CCCD',
            'address':'Địa chỉ',
            'type_customer':'Loại khách hàng',
            'special_info': 'note',
      }
      def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class EmployeeView(AuthenticatecModelView):
      column_display_pk = True
      column_searchable_list = ['full_name', 'phone', 'email', 'cccd']
      column_filters = ['full_name', 'phone', 'email', 'cccd', 'address']
      column_list  = ['id','full_name','phone', 'cccd', 'address', 'salary','start_date','user_id']
      form_columns  = ['full_name','phone', 'cccd', 'email', 'address', 'salary','start_date','user_id']
      column_editable_list = ['full_name', 'phone', 'email']
      can_export = True
      page_size = 10
      column_labels = {
            'id': 'ID',
            'full_name': 'Tên Nhân Viên',
            'phone': 'Số điện thoại',
            'cccd': 'CCCD',
            'address':'Địa chỉ',
            'salary':'Lương',
            'start_date': 'Ngày vào làm',
            'user_id': 'Tên đăng nhập',
      }
      def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class BookingDetailView(AuthenticatecModelView):
      column_display_pk = True
      
      form_column = ['id', 'date_in','date_out', 'customer_id', 'booking_id', 'room_id']
      column_searchable_list = ['date_in','date_out', 'customer_id', 'booking_id', 'room_id']
      column_filters = ['date_in','date_out', 'customer_id', 'booking_id', 'room_id']
      page_size = 10
      column_labels = {
            'id': 'ID',
            'date_in': 'Ngày thuê phòng',
            'date_out': 'Ngày trả phòng',
            'customer_id': 'mã khách hàng',
            'booking_id': 'mã đặt phòng',
            'room_id': 'mã phòng',
            'discount': 'mã giảm giá',
            'delete': 'Xóa'
      }
      
      def is_accessible(self):
            return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class RentalReceiptView(AuthenticatecModelView):
      column_display_pk = True
      column_formatters = {
            'total_amount': lambda v, c, m, p: f"{float(m.total_amount):,.1f}"
      }
      def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class PaymentView(AuthenticatecModelView):
      column_display_pk = True
      column_formatters = {
            'amount': lambda v, c, m, p: f"{float(m.amount):,.1f}"
      }
      def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

      




      def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class RentalDetailView(AuthenticatecModelView):
      column_display_pk = True

      def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


admin = Admin(app=app,
            name="Hotel Management", 
            template_mode='bootstrap4',
            index_view=MyAdminIndex())

class UploadForm(FlaskForm):
      file = FileField('Upload File', validators=[
            FileRequired(),
            FileAllowed(['jpg', 'png', 'pdf'], 'Only images and PDFs are allowed!')
      ])
      submit = SubmitField('Upload')

class BookingView(AuthenticatecModelView):
      # column_display_pk = True
      column_list = ('id', 'customer.full_name', 'booking_date')
      form_columns = {'id', 'created_date', 'total_customer', 'total_amount', 'customer_id', 'user_id'}
      column_searchable_list = ['created_date', 'total_customer', 'customer_id', 'user_id']
      column_filters = ['created_date', 'total_customer', 'customer_id', 'user_id']
      column_editable_list = ['created_date', 'total_customer', 'total_amount', 'customer_id', 'user_id']
      can_export = True
      page_size = 10
      
      column_labels = {
            'id': 'ID',
            'created_date': 'Ngày tạo',
            'total_customer': 'Số khách',
            'total_amount': 'Tổng tiền',
            'customer_id': 'Mã khách hàng',
            'order_type_id': 'Loại phòng',
            'user_id': 'Mã người dùng',
      }
      def is_accessible(self):
            return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN
# Tổ chức các danh mục
admin.add_view(UserView(User, db.session,name="Tài khoản", category="Quản lý người dùng"))
admin.add_view(customerView(Customer, db.session,name="Khách hàng", category="Quản lý người dùng"))
admin.add_view(EmployeeView(Employee, db.session,name="Nhân Viên", category="Quản lý người dùng"))

admin.add_view(RoomView(Room, db.session, category="Quản lý phòng"))

admin.add_view(BookingView(Booking, db.session, category="Quản lý đặt phòng"))
admin.add_view(BookingDetailView(BookingDetail, db.session, category="Quản lý đặt phòng"))

admin.add_view(RentalReceiptView(RentalReceipt, db.session, category="Quản lý hóa đơn"))
admin.add_view(PaymentView(Payment, db.session, category="Quản lý hóa đơn"))

admin.add_view(RentalDetailView(RentalDetail, db.session, name="Chi tiết phiếu thuê", category="Phiếu thuê"))


admin.add_view(StatisticView(name='Thống Kê', endpoint='thong_ke', category="Thống kê"))
admin.add_view(StatisticView(name='Báo cáo Doanh Thu', endpoint='bao_cao_doanh_thu', category="Thống kê"))
admin.add_view(StatisticView(name='Mật Độ Sử Dụng Phòng', endpoint='mat_do_su_dung_phong', category="Thống kê"))
admin.add_view(PaymentConfirmation(name='Xác Nhận Thanh toán'))
admin.add_view(RentalRoom(name='Lập Phiếu Thuê Phòng'))
admin.add_view(LogoutView(name='Logout'))


