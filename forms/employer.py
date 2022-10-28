from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo


class EmployerForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=20)])
    description = TextAreaField('Description', validators=[InputRequired()])
    submit =SubmitField('Submit')