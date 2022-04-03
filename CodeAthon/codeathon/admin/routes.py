from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from codeathon import db, bcrypt
from codeathon.models import Contest, Submission, Role, Team, Challenge, User
from codeathon.admin.forms import ContestForm
from faker import Faker

admin = Blueprint("admin", __name__)


@admin.route("/contest/new", methods=["GET", "POST"])
@login_required
def new_contest():
    if current_user.role.id != 3:
        abort(403)
    form = ContestForm()
    if form.validate_on_submit():
        contest = Contest(
            title=form.title.data,
            description=form.description.data,
            start_date_time=form.start_date_time.data,
            end_date_time=form.end_date_time.data,
        )
        db.session.add(contest)
        db.session.commit()
        flash("Your contest has been created!", "success")
        return redirect(url_for("admin.contest", contest_id=contest.id))
    return render_template(
        "admin/create_contest.html",
        title="New Contest",
        form=form,
        legend="New Contest",
    )


@admin.route("/contest/<int:contest_id>")
def contest(contest_id):
    contest = Contest.query.get_or_404(contest_id)
    return render_template("admin/contest.html", title=contest.title, contest=contest)


@admin.route("/contest/<int:contest_id>/update", methods=["GET", "POST"])
@login_required
def update_contest(contest_id):
    if current_user.role.id != 3:
        abort(403)
    contest = Contest.query.get_or_404(contest_id)
    form = ContestForm()
    if form.validate_on_submit():
        contest.title = form.title.data
        contest.description = form.description.data

        db.session.commit()
        flash("Your contest has been updated!", "success")
        return redirect(url_for("admin.contest", contest_id=contest.id))
    elif request.method == "GET":
        form.title.data = contest.title
        form.content.data = contest.content
    return render_template(
        "create_contest.html",
        title="Update Contest",
        form=form,
        legend="Update Contest",
    )


@admin.route("/contest/<int:contest_id>/delete", methods=["POST"])
@login_required
def delete_contest(contest_id):
    if current_user.role.id != 3:
        abort(403)
    contest = Contest.query.get_or_404(contest_id)
    db.session.delete(contest)
    db.session.commit()
    flash("Your contest has been deleted!", "success")
    return redirect(url_for("main.home"))


@admin.route("/create_fake_users")
@login_required
def create_fake_users():
    """Generate fake users."""
    if current_user.role.id != 3:
        abort(403)
    faker = Faker()
    hashed_password = bcrypt.generate_password_hash("test").decode("utf-8")
    for i in range(25):
        fname = faker.first_name()
        lname = faker.last_name()
        uname = fname + lname
        user = User(
            username=uname,
            first_name=fname,
            last_name=lname,
            image_file="default.jpg",
            password=hashed_password,
            role_id="1",
            email=faker.email(),
        )
        db.session.add(user)
    db.session.commit()
    flash("Your users have been created!", "success")
    return redirect(url_for("main.home"))
