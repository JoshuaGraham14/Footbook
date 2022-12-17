from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
# Handles all migrations.
# migrate = Migrate(app, db)
migrate = Migrate(app, db, render_as_batch=True)

from app import views, models
