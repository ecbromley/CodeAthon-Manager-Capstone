from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms.fields import DateTimeLocalField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ContestForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    start_date_time = DateTimeLocalField(
        "Start Date and Time", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    end_date_time = DateTimeLocalField(
        "End Date and Time", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    submit = SubmitField("Add")
