from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length

from utilities.fields import get_fields

class ProviderForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=20)])
    description = TextAreaField('Description', validators=[InputRequired()])
    field = SelectField('Field', validators=[InputRequired()], choices=get_fields())
    submit =SubmitField('Submit')

class SkillForm(FlaskForm):
    skills = StringField('Skills: Enter a comma separated list of your skills...', validators=[InputRequired()])
    submit =SubmitField('Submit')