from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = 'sdifnsdaifjnu5862#$%@$%@&dfgfdgj'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:%s@localhost/khachsandb?charset=utf8mb4' % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
cloudinary.config(cloud_name='dmt3j04om',
                api_key='358476894396759',
                api_secret='BJB1D2g3nRAdPtErPMYLIELEuyM')

login = LoginManager(app=app)

db = SQLAlchemy(app=app)
