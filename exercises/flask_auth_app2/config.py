import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'secret-key-goes-here'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True