WTF_CSRF_ENABLED = True
SECRET_KEY = 'a-very-secret-elephant'

#if deployed keep session_cookie_secure as True
SESSION_COOKIE_SECURE = True


import os


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
