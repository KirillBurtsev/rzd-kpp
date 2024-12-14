from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
app = Flask(__name__)

app.config['SECRET_KEY']='someinstanse'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://employee:12345678@localhost:5432/gate'

db=SQLAlchemy(app)
# bcrypt=Bcrypt(app)
# login_manager=LoginManager(app)

from rzd_kpp import routes

