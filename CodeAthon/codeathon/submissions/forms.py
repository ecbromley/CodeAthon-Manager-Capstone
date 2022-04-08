from flask import g
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms.fields import DateTimeLocalField
from wtforms import PasswordField, StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    ValidationError,
    NumberRange,
    EqualTo,
)
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from codeathon.models import User, Contest
