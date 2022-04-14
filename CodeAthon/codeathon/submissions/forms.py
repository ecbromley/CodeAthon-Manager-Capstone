from flask import g
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class SubmissionForm(FlaskForm):
    challenge = SelectField("Challenge", choices=[], validators=[DataRequired()])
    language = SelectField("Language", choices=[], validators=[DataRequired()])
    code = FileField("Code")
    code_output = FileField("Result")
    Score = IntegerField("Score")
    submit = SubmitField("Submit")
