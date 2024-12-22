from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'sasdfasdf2#$%@$%@&dfgfdgj'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:%s@localhost/khachsandb?charset=utf8mb4' % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.permanent_session_lifetime = timedelta(days=1)
cloudinary.config(cloud_name='dmt3j04om',
            api_key='358476894396759',
            api_secret='BJB1D2g3nRAdPtErPMYLIELEuyM')

app.config['PAGE_SIZE'] = 4

login = LoginManager(app=app)

db = SQLAlchemy(app=app)
