from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

admin = Admin(app,template_mode='bootstrap4')

from app import views, models