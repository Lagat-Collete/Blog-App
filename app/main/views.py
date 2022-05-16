from curses import flash
from email.message import EmailMessage
from flask import render_template,request,redirect,url_for,abort
from flask_login import login_required,current_user
from requests import get_quotes
from app.email import mail_message
from app.main.forms import PostForm, createPost
from .. import db,photos
from . import main
from .. models import Comment, Post, Subscriber, User





@main.route('/')
def index():
    quotes = get_quotes()
    return render_template("index.html",quote = quotes)

@main.route('/new-post', methods=['GET','POST'])
def new_post():
  form = PostForm()

  if form.validate_on_submit():
      post = Post(title=form.title.data, content=form.content.data, author=form.author.data)
      post.save()
      for subscriber in Subscriber:
            EmailMessage("New  Post","email/new_post",subscriber.email,post=post)
      return redirect(url_for('main.index'))
  flash('You Posted a new Post')
  return render_template('newpost.html', form = form)
    # #clear the form
    # form.title.data = ''
    # form.content.data = ''
    # form.author.data = ''

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
    form = createPost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("You have updated your post!")
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
    new_subscriber.save_subscriber()
    mail_message("Subscribed to Blog-Site","email/welcome_subscriber",new_subscriber.email,new_subscriber=new_subscriber)
    flash('Sucessfuly subscribed')
    return redirect(url_for('main.index'))

@main.route('/user/<string:username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(user=user).order_by(Post.posted.desc())
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
      

    
