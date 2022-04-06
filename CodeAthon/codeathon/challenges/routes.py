from flask import render_template, request, Blueprint
from codeathon.models import Challenge

challenges = Blueprint("challenges", __name__)


@challenges.route("/challenges")
def home():

    return render_template("challenges.html")
