from email.policy import default
from requests import post
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,current_user
from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),unique = True,nullable = False)
    email = db.Column(db.String(255), unique = True,nullable = False)
    bio = db.Column(db.String(255),default ='default bio')
    profile_pic_path = db.Column(db.String(),default ='default.png')
    password_hash = db.Column(db.String(255),nullable = False)
    post = db.relationship('Post', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannnot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
        
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'User {self.username}'


class Post(db.Model):
    __tablename__='posts'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255),nullable=False)
    content = db.Column(db.Text(),nullable=False)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comment = db.relationship('Comment', backref='post', lazy='dynamic')


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

    def get_post(id):
        post =Post.query.filter_nby(id=id).first()

        return post

    def __repr__(self):
        return f'Post {self.title}'

class Comment(db.Model):
    __tablename__='comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    post_id = db.Column(db.Integer,db.ForeignKey("posts.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

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


    
class Subscriber(db.Model):
    __tablename__='subscribers'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255),unique=True, index=True)

    def save_subscriber(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Subscriber {self.email}'

    
class Quotes:
    def __init__(self,author,quote):
        self.author = author
        self.quote = quote 
    

