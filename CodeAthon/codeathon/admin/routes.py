from flask import (
    abort,
    Blueprint,
    flash,
    g,
    redirect,
    request,
    render_template,
    url_for,
)
from faker import Faker
from flask_login import current_user, login_required
from io import BytesIO
from werkzeug.utils import secure_filename
from codeathon import db, bcrypt
from codeathon.models import Contest, Submission, Role, Team, User
from codeathon.admin.forms import (
    AddUserForm,
    AdminUpdateUserForm,
    ContestForm,
    ContestFormUpdate,
)


admin = Blueprint("admin", __name__)

#######Contests#######
@admin.route("/contest/new", methods=["GET", "POST"])
@login_required
def new_contest():
    if current_user.user_role.id != 3:
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
        "admin/contest_add.html",
        title="New Contest",
        form=form,
        legend="New Contest",
    )


@admin.route("/contest/<int:contest_id>")
def contest(contest_id):
    contest = Contest.query.get_or_404(contest_id)
    return render_template("admin/contest.html", title=contest.title, contest=contest)


@admin.route("/contests_table")
@login_required
def contests_table():
    if current_user.user_role.id != 3:
        abort(403)
    contests = Contest.query
    return render_template(
        "admin/contests_table.html", title="Contests Table", contests=contests
    )


@admin.route("/contest/<int:contest_id>/update", methods=["GET", "POST"])
@login_required
def update_contest(contest_id):
    if current_user.user_role.id != 3:
        abort(403)
    contest = Contest.query.get_or_404(contest_id)
    form = ContestFormUpdate()
    if form.validate_on_submit():
        contest.title = form.title.data
        contest.description = form.description.data
        contest.start_date_time = form.start_date_time.data
        contest.end_date_time = form.end_date_time.data

        db.session.commit()
        flash("Your contest has been updated!", "success")
        return redirect(url_for("admin.contest", contest_id=contest.id))
    elif request.method == "GET":
        form.title.data = contest.title
        form.description.data = contest.description
        form.start_date_time.data = contest.start_date_time
        form.end_date_time.data = contest.end_date_time
    return render_template(
        "admin/contest_add.html",
        title="Update Contest",
        form=form,
        legend="Update Contest",
    )


@admin.route("/contest/<int:contest_id>/delete", methods=["POST"])
@login_required
def delete_contest(contest_id):
    if current_user.user_role.id != 3:
        abort(403)
    contest = Contest.query.get_or_404(contest_id)
    db.session.delete(contest)
    db.session.commit()
    flash("Your contest has been deleted!", "success")
    return redirect(url_for("main.home"))


#######Languages#######


#######Teams#######


#######Users#######
@admin.route("/users_table")
def users_table():
    if current_user.user_role.id != 3:
        abort(403)
    users = User.query
    return render_template("admin/users_table.html", title="Users Table", users=users)


@admin.route("/user_add", methods=["GET", "POST"])
def user_add():
    if current_user.user_role.id != 3:
        abort(403)
    form = AddUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data,
        )
        db.session.add(user)
        db.session.commit()
        flash("The user has been created!", "success")
        return redirect(url_for("admin.users_table"))
    return render_template("admin/user_add.html", title="Register", form=form)


@admin.route("/create_fake_users")
@login_required
def create_fake_users():
    """Generate fake users."""
    if current_user.user_role.id != 3:
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
            role="1",
            email=faker.email(),
        )
        db.session.add(user)
    db.session.commit()
    flash("Your users have been created!", "success")
    return redirect(url_for("admin.users_table"))


@admin.route("/user/<string:username>", methods=["GET", "POST"])
@login_required
def user_admin(username):
    if current_user.user_role.id != 3:
        abort(403)
    user = User.query.filter_by(username=username).first_or_404()
    form = AdminUpdateUserForm()
    g.user = user
    if form.validate_on_submit():
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
                "utf-8"
            )
            current_user.password = hashed_password
        if form.picture.data:
            picture_file = user.save_picture(form.picture.data)
            user.image_file = picture_file
        user.username = form.username.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.role = form.role.data
        db.session.commit()
        flash("The user account has been updated!", "success")
        return redirect(url_for("admin.users_table"))
    elif request.method == "GET":
        form.id.data = user.id
        form.username.data = user.username
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.email.data = user.email
        form.role.data = user.role
    image_file = url_for("static", filename="profile_pics/" + user.image_file)
    return render_template(
        "admin/user.html", title="User", image_file=image_file, form=form, user=user
    )


@admin.route("/user/<int:user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    if current_user.user_role.id != 3:
        abort(403)
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("The user has been deleted!", "success")
    return redirect(url_for("admin.users_table"))
