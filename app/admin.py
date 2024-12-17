from flask_admin import Admin
from app import app, db
from app.models import User, Person, Customer, Employee, Booking, Room, BookingDetail, RentalReceipt, Payment, RentalDetail, RentalCustomer
from flask_admin.contrib.sqla import ModelView


admin = Admin(app = app, name="Hotel Management", template_mode='bootstrap4')

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

class RoomView (ModelView):
      column_display_pk = True
      column_searchable_list = [ 'name', 'price','max_customer', 'type_room']
      column_filters = ['name', 'price','max_customer','status', 'type_room','booking_details']
      column_editable_list = ['name', 'max_customer','price','status', 'type_room',  "image"]
      can_export = True
      page_size = 10
      
class PersonView (ModelView):
      column_display_pk = True
      column_searchable_list = ['full_name', 'phone', 'email']
      column_filters = ['full_name', 'phone', 'email', 'cccd', 'address']
      column_editable_list = ['full_name', 'phone', 'email']
      can_export = True
      page_size = 10

# Tổ chức các danh mục
admin.add_view(UserView(User, db.session, category="Quản lý người dùng"))
admin.add_view(PersonView(Person, db.session, category="Quản lý người dùng"))
admin.add_view(ModelView(Customer, db.session, category="Quản lý người dùng"))
admin.add_view(ModelView(Employee, db.session, category="Quản lý người dùng"))

admin.add_view(RoomView(Room, db.session, category="Quản lý phòng"))

admin.add_view(ModelView(Booking, db.session, category="Quản lý đặt phòng"))
admin.add_view(ModelView(BookingDetail, db.session, category="Quản lý đặt phòng"))

admin.add_view(ModelView(RentalReceipt, db.session, category="Quản lý hóa đơn"))
admin.add_view(ModelView(Payment, db.session, category="Quản lý hóa đơn"))

admin.add_view(ModelView(RentalDetail, db.session, category="Quản lý thuê phòng"))
admin.add_view(ModelView(RentalCustomer, db.session, category="Quản lý thuê phòng"))




