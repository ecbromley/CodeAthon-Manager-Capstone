from io import BytesIO
from flask import (
    abort,
    Blueprint,
    flash,
    g,
    redirect,
    request,
    render_template,
    send_file,
    url_for,
)
from faker import Faker
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from codeathon import db, bcrypt
from codeathon.models import Contest, Submission, Role, Team, Challenge, User


submissions = Blueprint("submissions", __name__)
