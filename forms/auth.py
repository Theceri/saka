import email_validator
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo

class LogInForm(FlaskForm):
    email = StringField('Email Address', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')
    submit =SubmitField('Log in')

class RegisterForm(FlaskForm):
    full_name = StringField('Full Name', validators=[InputRequired(), Length(min=4, max=20)])
    phone = StringField('Phone', validators=[InputRequired(), Length(min=10, max=12)])
    email = StringField('Email Address', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('password_confirm', message='Passwords do not match!')])
    password_confirm = PasswordField('Retype Password')
    submit =SubmitField('Sign Up')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email Address', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    submit =SubmitField('Send Link')

class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('password_confirm', message='Passwords do not match!')])
    password_confirm = PasswordField('Retype Password')
    submit =SubmitField('Reset')


