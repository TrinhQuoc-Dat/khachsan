from app.models import UserRole

def get_user_role(key):
    if key.__eq__('USER'):
        return UserRole.USER
    elif key.__eq__('ADMIN'):
        return UserRole.ADMIN
    return UserRole.EMPLOYEE

def count_customer(cart):
    return sum(int(c['number_customer']) for c in cart.values())
