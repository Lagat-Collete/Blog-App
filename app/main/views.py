from curses import flash
from email.message import EmailMessage
from flask import render_template,request,redirect,url_for,abort
from flask_login import login_required,current_user
from requests import get_quotes
from app.main.forms import PostForm
from .. import db,photos
from . import main
from .. models import Post, Subscriber, User





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

@main.route('/blog/update/<blog_id>', methods = ['GET','POST'])
@login_required
def update_blog(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    form = CreateBlog()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.content = form.content.data
        db.session.commit()
        flash("You have updated your Blog!")
        return redirect(url_for('main.blog',id = blog.id)) 
    if request.method == 'GET':
        form.title.data = blog.title
        form.content.data = blog.content
    return render_template('newblog.html', form = form)

@main.route('/comment/<blog_id>', methods = ['Post','GET'])
@login_required
def comment(blog_id):
    blog = Blog.query.get(blog_id)
    if request.method == 'POST':
        comment =request.form.get('newcomment')
        new_comment = Comment(comment = comment, user_id = current_user._get_current_object().id, blog_id=blog_id)
        new_comment.save()
    return redirect(url_for('main.blog',blog_id = blog.id))    

@main.route('/subscribe',methods = ['POST','GET'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscriber = Subscriber(email = email)
    new_subscriber.save_subscriber()
    mail_message("Subscribed to D-Blog","email/welcome_subscriber",new_subscriber.email,new_subscriber=new_subscriber)
    flash('Sucessfuly subscribed')
    return redirect(url_for('main.index'))

@main.route('/user/<string:username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page',1, type = int )
    blogs = Blog.query.filter_by(user=user).order_by(Blog.posted.desc()).paginate(page = page, per_page = 4)
    return render_template('userposts.html',blogs=blogs,user = user)

@main.route('/blog/<blog_id>/delete', methods = ['POST'])
@login_required
def delete_post(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    blog.delete()
    flash("Blog deleted succesfully!")
    return redirect(url_for('main.index'))
      

    
