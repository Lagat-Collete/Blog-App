from curses import flash
from flask import render_template,request, redirect,url_for
from flask_login import login_user,logout_user,login_required
from app.auth import auth
from app. models import User
from .forms import SigninForm,SignupForm
from ..email import mail_message
from .. import db


@auth.route('/signin', methods =['POST', 'GET'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user != None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Incorrect Username or Password')

    return render_template('signin.html',form = form)

@auth.route('/signup', methods =['POST', 'GET'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email = form.email.data, password=form.password.data)
        print('outside', user)
        if user != None and user.verify_password(form.password.data):
           print('inside', user)
           db.session.add(user)
           db.session.commit()
        mail_message("Hello,Welcome to my Blog site","email/welcome_user",user.email,user=user)
        return  redirect(url_for('auth.signin'))
    print('outside validation', form)
    return render_template('signup.html', form=form )
  
@auth.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for("main.index"))
    
@auth.route('/subscribe',methods=['GET','POST'])
def subscribe():
    title = 'subscribe to My Blog site'
    return render_template('subscribe.html',title=title)