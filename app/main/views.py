from crypt import methods
from curses import flash
from turtle import title
from flask import render_template,request,redirect,url_for,abort
from flask_login import login_required,current_user

from app.main.forms import PostForm
from .. import db,photos
from . import main
from .. models import Posts, User





@main.route('/')
@login_required
def index():
  title = 'title is here'
  return render_template("index.html")

@main.route('/add-post', methods=['GET','POST'])
def add_post():
  form = PostForm()

  if form.validate_on_submit():
      post = Posts(title=form.title.data, content=form.content.data, author=form.author.data)
      #clear the form
      form.title.data = ''
      form.content.data = ''
      form.author.data = ''

      

      flash('Blog Submitted Successfully,Thank you.')

  return render_template('add_post.html', form=form)

