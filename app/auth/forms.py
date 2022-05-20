from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, IntegerField,SubmitField,ValidationError
from wtforms.validators import InputRequired,Length,Email
from ..models import User



class SigninForm(FlaskForm):
  username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
  password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=25)])
  remember = BooleanField('remember me')
  submit =  SubmitField('Login')

class SignupForm(FlaskForm):
  email = StringField('email', validators=[InputRequired(),Email(), Length(min=10, max =80)])
  username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
  password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=25)])
  password_confirm =PasswordField('password_confirm', validators=[InputRequired(), Length(min=8, max=25)])
  submit = SubmitField('SignUp')
  
  def validate_email(self,data_field):
      print( ' DATA', data_field)

      if User.query.filter_by(email = data_field.data).first():
        
          raise ValidationError("The Email has already been taken!")
       
  def validate_username(self, data_field):
      if User.query.filter_by(username = data_field.data).first():
            raise ValidationError("The username has already been taken")


     
