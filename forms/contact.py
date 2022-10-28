import email_validator
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField
from wtforms.validators import InputRequired, Email, Length
from flask_ckeditor.fields import CKEditorField


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=30)])
    email = StringField('Your Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    subject = StringField('Subject', validators=[InputRequired(), Length(min=4, max=50)])
    message = TextAreaField('Message', validators=[InputRequired()])
    submit =SubmitField('Submit')

class ReplyForm(FlaskForm):
    message = CKEditorField('Message', validators=[InputRequired()])
    submit =SubmitField('Submit')