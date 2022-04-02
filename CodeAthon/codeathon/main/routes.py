from flask import render_template, request, Blueprint
from flask_login import current_user
from codeathon.models import Contest

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    # page = request.args.get("page", 1, type=int)
    contest = Contest.query.order_by(Contest.start_date_time.desc()).first()
    return render_template("home.html", contest=contest)


@main.route("/about")
def about():
    return render_template("about.html", title="About")
