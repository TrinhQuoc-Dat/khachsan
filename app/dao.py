from app.models import User, UserRole
from app import app, db, login
import hashlib

def check_user(username, password, role=UserRole.USER):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password),
                             User.user_role.__eq__(role)).first()
@login.user_loader
def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_username(username):
    return User.query.filter(User.username.__eq__(username)).first()


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

if __name__ == '__main__':
    with app.app_context():
        u = check_user(username='dat', password=str(123), role=UserRole.USER)
        print(u)

