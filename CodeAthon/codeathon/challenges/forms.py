from flask import g
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class ChallengeForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    supportzip = FileField("Add Support File", validators=[FileAllowed(["zip"])])
    code_scorer = FileField("Add Scorer File")
    dockerfile = FileField("Add Docker File")
    submit = SubmitField("Add")


class ChallengeFormUpdate(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    supportzip = FileField("Update Support File", validators=[FileAllowed(["zip"])])
    code_scorer = FileField("Update Scorer File")
    dockerfile = FileField("Update Docker File")
    submit = SubmitField("Update")
