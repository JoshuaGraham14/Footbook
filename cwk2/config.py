import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'joshuagraham'
SESSION_COOKIE_SECURE = True

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True