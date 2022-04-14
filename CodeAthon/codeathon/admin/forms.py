from flask import g
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms.fields import DateTimeLocalField
from wtforms import (
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
    IntegerField,
    SelectField,
    BooleanField,
)
from wtforms.validators import (
    AnyOf,
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

# from codeathon.admin.routes import compareform


class ChallengeForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = CKEditorField("Description", validators=[DataRequired()])
    supportzip = FileField("Add Support File", validators=[FileAllowed(["zip"])])
    code_scorer = FileField("Add Scorer File")
    dockerfile = FileField("Add Docker File")
    submit = SubmitField("Add")


class ChallengeFormUpdate(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = CKEditorField("Description", validators=[DataRequired()])
    supportzip = FileField("Update Support File", validators=[FileAllowed(["zip"])])
    code_scorer = FileField("Update Scorer File")
    dockerfile = FileField("Update Docker File")
    submit = SubmitField("Update")


class ContestForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = CKEditorField("Description", validators=[DataRequired()])
    start_date_time = DateTimeLocalField(
        "Start Date and Time", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    end_date_time = DateTimeLocalField(
        "End Date and Time", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    active = BooleanField("Active")
    submit = SubmitField("Add")

    def validate_active(self, active):
        active = Contest.query.filter_by(active=True).first()
        if active:
            raise ValidationError(
                "A contest is already active, only one contest may be active at one time."
            )


class ContestFormUpdate(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = CKEditorField("Description", validators=[DataRequired()])
    start_date_time = DateTimeLocalField(
        "Start Date and Time", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    end_date_time = DateTimeLocalField(
        "End Date and Time", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    active = BooleanField("Active")
    submit = SubmitField("Update")

    def validate_active(self, active):
        active = Contest.query.filter_by(active=True).first()
        if active:
            raise ValidationError(
                "A contest is already active, only one contest may be active at one time."
            )


class LanguageForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Add")


class LanguageFormUpdate(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Update")


class TeamForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    contest = SelectField("Contest", choices=[], validators=[DataRequired()])
    submit = SubmitField("Add")


class TeamFormUpdate(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    contest = SelectField("Contest", choices=[], validators=[DataRequired()])
    submit = SubmitField("Update")


class AddUserForm(FlaskForm):
    id = IntegerField()
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    role = IntegerField("Role", validators=[NumberRange(min=1, max=3)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Add User")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class AdminUpdateUserForm(FlaskForm):
    id = IntegerField()
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    role = IntegerField("Role", validators=[NumberRange(min=1, max=3)])
    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "jpeg", "png"])]
    )
    password = PasswordField("Password")
    confirm_password = PasswordField(
        "Confirm Password", validators=[EqualTo("password")]
    )
    submit = SubmitField("Update")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            if g.user.username != username.data:
                raise ValidationError(
                    "That username is taken. Please choose a different one."
                )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            if g.user.email != email.data:
                raise ValidationError(
                    "That email is taken. Please choose a different one."
                )
