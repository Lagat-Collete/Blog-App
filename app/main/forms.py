from turtle import title
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Write a brief bio about you.',validators = [DataRequired()])
    submit = SubmitField('Save')



class PostForm(FlaskForm):
  title = StringField("Title", validators=[DataRequired()])
  content = StringField("Content",validators=[DataRequired()],widget=TextArea())
  author = StringField("Author",validators=[DataRequired()])
  submit = StringField('Post')