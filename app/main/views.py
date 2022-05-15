from turtle import title
from flask import render_template,request,redirect,url_for,abort
from flask_login import login_required,current_user
from .. import db,photos
from . import main
from .. models import User





@main.route('/')
@login_required
def index():
  title = 'title is here'
  return render_template("index.html")