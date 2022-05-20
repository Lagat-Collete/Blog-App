
from flask import render_template,redirect,url_for,abort,request,flash
from app.main import main
from .. import db
from app.models import User,Post,Comment,Subscriber
from app.requests import get_quotes
import secrets
import os
from flask_login import login_required,current_user
from .forms import UpdateProfile,CreatePost
from ..email import mail_message



@main.route('/')
def index():
    quotes = get_quotes()
    page = request.args.get('page',1, type = int )
    posts = Post.query.all()
    return render_template('index.html', quote = quotes,posts=posts)

@main.route('/profile',methods = ['POST','GET'])
@login_required
def profile():
    form = UpdateProfile()
    profile_pic_path = ''
    print('CURRENT', current_user)
    if form.validate_on_submit():
        if form.profile_picture.data:
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.bio = form.bio.data
            db.session.commit()
            flash('Succesfully updated your profile')
            return redirect(url_for('profile'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
            form.bio.data = current_user.bio
            profile_pic_path = url_for('static',filename ='images/'+ current_user.profile_pic_path) 
    return render_template('profile.html', profile_pic_path = profile_pic_path, form = form)    

@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username = name).first()
    if user == None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save()
        return redirect(url_for('.profile',name = name))
    return render_template('updateprofile.html',form =form)



@main.route('/new-post', methods=['GET','POST'])
@login_required
def new_post():
  subscribers = Subscriber.query.all()
  form = CreatePost()
  if form.validate_on_submit():
      title = form.title.data
      content = form.content.data
      author =form.author.data
      user_id = current_user._get_current_object().id
      post = Post(title=title, content=content, author=author, user_id =user_id)
      post.save()
      for subscriber in subscribers:
            mail_message("New  Post","email/new_post",subscriber.email,post=post)
      return redirect(url_for('main.index'))
  flash('You Posted a new Post')
  return render_template('newpost.html', form = form)
    

@main.route('/post/<post_id>', methods = ['GET'])
@login_required
def post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', post = post)

@main.route('/post/update/<post_id>', methods = ['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get(post_id)
    if post.user != current_user:
        abort(403)
    form = CreatePost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("You have updated your Post!")
        return redirect(url_for('main.post',id = post.id)) 
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('newpost.html', form = form)

@main.route('/comment/<post_id>', methods = ['Post','GET'])
@login_required
def comment(post_id):
    post = Post.query.get(post_id)
    if request.method == 'POST':
        comment =request.form.get('newcomment')
        new_comment = Comment(comment = comment, user_id = current_user._get_current_object().id, post_id=post_id)
        new_comment.save()
    return redirect(url_for('main.post',post_id= post.id))    

@main.route('/subscribe',methods = ['POST','GET'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscriber = Subscriber(email = email)
    mail_message("Subscribed to Blog-Site","email/welcome_subscriber",new_subscriber.email,new_subscriber=new_subscriber)
    flash('Sucessfuly subscribed')
    return redirect(url_for('main.index'))

@main.route('/user/<string:username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page',1, type = int )
    posts = Post.query.filter_by(user=user).order_by(Post.posted.desc()).paginate(page = page, per_page = 4)
    return render_template('userposts.html',posts=posts,user = user)

@main.route('/post/<post_id>/delete', methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post.user != current_user:
        abort(403)
    post.delete()
    flash("Post deleted succesfully!")
    return redirect(url_for('main.index'))
      

    
