import os

WTF_CSRF_ENABLED = True
SECRET_KEY = '1BCDEFGHIJKLMNOPQRSTUVWXYZ12345'


basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db?check_same_thread=False')
SQLALCHEMY_TRACK_MODIFICATIONS = True
