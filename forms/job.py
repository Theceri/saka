from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length
from flask_ckeditor.fields import CKEditorField
from utilities.fields import get_fields


class FieldForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=3, max=20)])
    submit =SubmitField('Submit')


class JobForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=50)])
    description = CKEditorField('Description', validators=[InputRequired()])
    qualifications = CKEditorField('Qualifications', validators=[InputRequired()])
    field = SelectField('Field', validators=[InputRequired()], choices=get_fields())
    submit =SubmitField('Submit')