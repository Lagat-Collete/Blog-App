from email.policy import default
from turtle import title

from requests import post
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),unique = True,nullable = False)
    email = db.Column(db.String(255), unique = True,nullable = False)
    bio = db.Column(db.String(255),default ='default bio')
    profile_pic_path = db.Column(db.String(),default ='default.png')
    password_hash = db.Column(db.String(255),nullable = False)
    photos = db.relationship('PhotoProfile',backref = 'user',lazy = "dynamic")
    @property
    def password(self):
        raise AttributeError('You cannnot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
        
    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'User {self.username}'


class Comment(db.Model):
    __tablename__='comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

    def get_comment(id):
        comment = Comment.query.all(id=id)
        return comment

    def __repr__(self):
        return f'Comment {self.comment}'



class Posts(db.Model):
    __tablename__='posts'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()
    

    
class Quotes:
    def __init__(self,author,quote):
        self.author = author
        self.quote = quote 
    

