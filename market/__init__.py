from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import Enum

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///market.db"
app.config['SECRET_KEY'] = 'd843990ef0dfa55e935a4e75'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
login = LoginManager(app)

from market import routes
