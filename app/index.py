import hashlib

from app import app, db, dao, utils
from flask import render_template, request, redirect, jsonify, url_for
from app.models import UserRole
from flask_login import login_user, logout_user, current_user


@app.route('/')
def home():
    return render_template('index.html')



@app.route('/login', methods=['post', 'get'])
def login():
    err_mgs = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user_role = request.form.get('user-role')
        try:
            u = dao.check_user(username=username, password=password,
                               role=utils.get_user_role(user_role))
            print(u)
            if u:
                login_user(user=u)
                return redirect('/')
            else:
                err_mgs = "username hoặc mật khẩu không đúng!!!"
        except Exception as ex:
            err_mgs = 'Error server' + str(ex)

    return render_template('login.html',
                           roles=UserRole,
                           err_mgs=err_mgs)


@app.route('/sign-out')
def logout():
    logout_user()
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(debug=True)

