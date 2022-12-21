from flask_login import UserMixin
from app import db

Friends = db.Table('Friends',
    db.Column('id', db.Integer,primary_key=True),
    db.Column('user_id1', db.Integer, db.ForeignKey('user.id')),
    db.Column('user_id2', db.Integer, db.ForeignKey('user.id')),
)

Likes = db.Table('Likes',
    db.Column('id', db.Integer,primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
)

Dislikes = db.Table('Dislikes',
    db.Column('id', db.Integer,primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(1000), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    team = db.Column(db.String(1000), nullable=False)
    posts = db.relationship('Post', backref='user', lazy='joined')
    friends =  db.relationship(
                    'User',secondary=Friends,
                    primaryjoin=Friends.c.user_id1==id,
                    secondaryjoin=Friends.c.user_id2==id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) #primary key 
    title = db.Column(db.String(200), nullable=False) #string max char length 200
    description = db.Column(db.String(1000), nullable=False) #string max char length 1000
    # timePosted = db.Column(db.DataTime, nullable=False) #DateTime data type
    # likes = db.Column(db.Integer, default=0) #Boolean data type
    # dislikes = db.Column(db.Integer, default=0) #Boolean data type
    likes = db.relationship('User', secondary=Likes, backref='liked')
    dislikes = db.relationship('User', secondary=Dislikes, backref='disliked')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)