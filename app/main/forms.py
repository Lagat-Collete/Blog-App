from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, TextAreaField, SubmitField,ValidationError
from wtforms.validators import DataRequired,InputRequired,Email
from flask_login import current_user
from wtforms.widgets import TextArea
from ..models import User


class UpdateProfile(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Address', validators=[InputRequired(),Email()])
    bio = TextAreaField('Bio',validators = [InputRequired()])
    profile_picture = FileField('profile picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_email(self,email):
        if email.data != current_user.email:
            if User.query.filter_by(email = email.data).first():
                raise ValidationError("The Email has already been taken!")
    
    def validate_username(self, username):
        if username.data != current_user.username:
            if User.query.filter_by(username = username.data).first():
                raise ValidationError("The username has already been taken")




class PostForm(FlaskForm):
  title = StringField("Title", validators=[DataRequired()])
  content = StringField("Content",validators=[DataRequired()],widget=TextArea())
  author = StringField("Author",validators=[DataRequired()])
  submit = StringField('Post')