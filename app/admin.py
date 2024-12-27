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

class RevenueStatsView(AuthenticatedView):
      @expose('/')
      def index(self, *args, **kwargs):

            return self.render('/admin/revenueStats.html', statsRevenue=dao.revenue_stats_Room(month=3, year=2024))

class FrequencyStatsView(AuthenticatedView):
      @expose('/')
      def index(self):
            return self.render('/admin/frequencyStats.html')

class OverviewStatsView(AuthenticatecModelView):
      @expose('/')
      def index(self):
            return self.render('admin/index.html')
      

class PaymentConfirmation(BaseView):
      @expose('/')
      def index(self, **kwargs):
            payment = dao.get_rental_payment()
            payment_dict = {}
            for p in payment:
                  rental_id, total_amount, created_date, customer_id = p[0], p[1], p[2], p[9]
                  detail = {
                        "room_id": p[3],
                        "customer_name": p[4],
                        "room_name": p[5],
                        "check_in_date": p[6],
                        "check_out_date": p[7],
                        "amount": p[8],
                        }
                  if rental_id not in payment_dict:
                    payment_dict[rental_id] = {
                        'rental_id': rental_id,
                        'total_amount': total_amount,
                        'created_date': created_date,
                        'customer_id': customer_id,
                        'details' : []
                  }
                    
                  payment_dict[rental_id]['details'].append(detail)
            return self.render('/admin/payment.html', payment_confirm = payment_dict)
      
      def is_accessible(self):
            return (current_user.is_authenticated and
                  current_user.user_role.__eq__(UserRole.EMPLOYEE))

class RentalRoom(BaseView):
    @expose('/')
    def index(self, **kwargs):
            if request.method.__eq__("post"):
                 pass
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
                        price = booking[4]
                        booking_detail_id = booking[5]
                        check_in_date = booking[6]
                        check_out_date = booking[7]
                        customer_id = booking[8]
                        customer_name = booking[9]
                        discount = booking[10]

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
                              'total_amount': price * discount * (check_out_date - check_in_date).days
                        }

            return self.render('/admin/RentalRoom.html', bookings=grouped_data)

    def is_accessible(self):
        return (current_user.is_authenticated and
                current_user.user_role.__eq__(UserRole.EMPLOYEE))

class MyAdminIndexView(AdminIndexView):
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
            'created_date': 'Ngày tạo'
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
      page_size = 5
      

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
      column_editable_list = ['full_name', 'cccd','phone', 'email']
      can_export = True
      page_size = 8
      column_labels = {
            'id': 'ID',
            'full_name': 'Tên khách hàng',
            'phone': 'Số điện thoại',
            'cccd': 'CCCD',
            'address':'Địa chỉ',
            'type_customer':'Loại khách hàng',
            'special_info': 'ghi chú',
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
      column_list = ['id','date_in','date_out', 'formatted_discount', 'room_id', 'booking_id','customer_id' ]
      form_column = ['id', 'date_in','date_out','discount', 'customer_id', 'booking_id', 'room_id']
      column_searchable_list = ['date_in','date_out', 'customer_id', 'booking_id', 'room_id']
      column_filters = ['date_in','date_out', 'customer_id', 'booking_id', 'room_id']
      page_size = 8
      column_exclude_list = ['delete']  # Ẩn cột delete
      column_labels = {
            'id': 'ID',
            'date_in': 'Ngày thuê phòng',
            'date_out': 'Ngày trả phòng',
            'customer_id': 'mã khách hàng',
            'booking_id': 'mã đặt phòng',
            'room_id': 'mã phòng',
            'discount': 'mã giảm giá',
            'delete': 'Xóa',
            'customer': 'Mã khách hàng',
            'booking': 'Mã đặt phòng',
            'room': 'Mã phòng',
            'formatted_discount': 'Mã giảm giá (%)'
      }
      
      def formatted_discount(self, context, model, name):
            if model.discount is None or model.discount == 1.0:
                  return "0%"
            return f"{round((1 - model.discount) * 100)}%"
      column_formatters = {
            'formatted_discount': formatted_discount
      }
      def is_accessible(self):
            return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class RentalReceiptView(AuthenticatecModelView):
      column_display_pk = True
      form_column = ['id', 'created_date', 'total_customer', 'note', 'total_amount','payments', 'employee_id', 'rental_details']
      column_searchable_list = ['created_date', 'total_customer','total_amount', 'employee_id']
      page_size = 8
      column_filters = ['created_date', 'total_customer', 'employee_id']
      column_labels = {
            'id': 'ID',
            'created_date': 'Ngày tạo',
            'total_customer': 'Tổng số lượng khách',
            'note': 'Ghi chú',
            'total_amount': 'Tổng số lượng',
            'payments': "Giá",
      }
      column_formatters = {
            'total_amount': lambda v, c, m, p: f"{float(m.total_amount):,.1f}"
      }
      def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class PaymentView(AuthenticatecModelView):
      column_display_pk = True
      form_column = ['id', 'created_date', 'type_payment', 'amount', 'status', 'note', 'rental_receipt_id']
      column_labels = {
            'id':  'ID',
            'created_date' : 'Ngày tạo',
            'type_payment': 'Phương thức thanh toán',
            'amount': 'tổng tiền',
            'status': 'trạng thái',
            'note': 'Ghi chú',
            'rental_receipt_id': 'mã biên lai cho thuê'
      }
      column_formatters = {
            'amount': lambda v, c, m, p: f"{float(m.amount):,.1f}"
      }
      def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

      def is_accessible(self):
            return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class RentalDetailView(AuthenticatecModelView):
      column_display_pk = True
      column_list = ['id', 'number_customer', 'date_in', 'date_out', 'total_amount', 'formatted_discount']
      form_columns = ['id', 'number_customer', 'date_in', 'date_out', 'total_amount', 'discount']
      column_exclude_list = ['quantity']
      column_searchable_list = ['date_in', 'date_out', 'rental_receipt_id', 'room_id']
      page_size = 8
      column_filters = ['number_customer', 'date_in', 'date_out', 'total_amount', 'discount', 'rental_receipt_id', 'room_id']
      column_labels = {
            'id': 'ID',
            'number_customer': 'Số lượng khách',
            'date_in': 'Ngày Thuê phòng',
            'date_out': 'Ngày trả phòng',
            'total_amount': 'Tổng tiền',
            'discount': 'Giảm giá',
            'formatted_discount': 'Giảm giá (%)'
      }
      column_formatters = {
            'total_amount': lambda v, c, m, p: f"{m.total_amount:,.1f}"
      }

      def formatted_discount(self, context, model, name):
            if model.discount is None or model.discount == 1.0:
                  return "0%"
            return f"{round((1 - model.discount) * 100)}%"

      column_formatters = {
            'formatted_discount': formatted_discount
      }
      def is_accessible(self):
            return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

admin = Admin(app=app,
            name="Hotel Management", 
            template_mode='bootstrap4',
            index_view=MyAdminIndexView())

class UploadForm(FlaskForm):
      file = FileField('Upload File', validators=[
            FileRequired(),
            FileAllowed(['jpg', 'png', 'pdf'], 'Only images and PDFs are allowed!')
      ])
      submit = SubmitField('Upload')

class BookingView(AuthenticatecModelView):
      column_display_pk = True
      column_list = ['id', 'created_date', 'total_customer', 'total_amount', 'order_type_id', 'customer']
      form_column = {'id', 'created_date', 'total_customer', 'total_amount', 'customer_id', 'order_type_id'}
      column_searchable_list = ['created_date', 'total_customer', 'customer_id', 'user_id']
      column_filters = ['created_date', 'total_customer', 'customer_id', 'user_id']
      column_editable_list = ['created_date', 'total_customer', 'total_amount', 'customer_id', 'user_id']
      column_exclude_list = ['employee_id', 'user_id']
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
            'employee_id': 'Mã nhân viên'
      }
      column_formatters = {
            'total_amount': lambda v, c, m, p: f"{m.total_amount:,.1f}"
      }
      
      def is_accessible(self):
            return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN
# Tổ chức các danh mục
admin.add_view(UserView(User, db.session,name="Tài khoản", category="Quản lý người dùng"))
admin.add_view(customerView(Customer, db.session,name="Khách hàng", category="Quản lý người dùng"))
admin.add_view(EmployeeView(Employee, db.session,name="Nhân Viên", category="Quản lý người dùng"))

admin.add_view(RoomView(Room, db.session,name = "Phòng", category="Quản lý phòng"))

admin.add_view(BookingView(Booking, db.session,name= 'Đặt phòng', category="Quản lý đặt phòng"))
admin.add_view(BookingDetailView(BookingDetail, db.session,name = "Chi tiết đặt phòng", category="Quản lý đặt phòng"))

admin.add_view(RentalReceiptView(RentalReceipt, db.session,name = "Biên lai", category="Quản lý hóa đơn"))
admin.add_view(PaymentView(Payment, db.session,name = "Thanh toán", category="Quản lý hóa đơn"))

admin.add_view(RentalDetailView(RentalDetail, db.session, name="Chi tiết phiếu thuê", category="Phiếu thuê"))


admin.add_view(RevenueStatsView(name='Báo cáo Doanh Thu',endpoint='revenueStats',category="Thống kê"))
admin.add_view(FrequencyStatsView(name='Mật Độ Sử Dụng Phòng',endpoint='frequencyStats',category="Thống kê"))
admin.add_view(PaymentConfirmation(name='Xác Nhận Thanh toán'))
admin.add_view(RentalRoom(name='Lập Phiếu Thuê Phòng'))
admin.add_view(LogoutView(name='Logout'))


