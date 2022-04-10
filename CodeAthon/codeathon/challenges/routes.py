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
from flask_login import current_user, login_required
from io import BytesIO
from codeathon import db
from codeathon.challenges.forms import (
    ChallengeForm,
    ChallengeFormUpdate,
)
from codeathon.models import Challenge

challenges = Blueprint("challenges", __name__)


@challenges.route("/challenges")
def home():

    return render_template("challenges.html")


@challenges.route("/challenge/new", methods=["GET", "POST"])
@login_required
def new_challenge():
    if current_user.user_role.id == 1:
        abort(403)
    form = ChallengeForm()
    challenge = Challenge()
    if form.validate_on_submit():
        challenge = Challenge(
            title=form.title.data,
            description=form.description.data,
            user_id=current_user.id,
        )
        if form.supportzip.data:
            challenge.supportzip_filename = form.supportzip.data.filename
            challenge.supportzip_data = form.supportzip.data.read()
        if form.code_scorer.data:
            challenge.code_scorer_filename = form.code_scorer.data.filename
            challenge.code_scorer_data = form.code_scorer.data.read()
        if form.dockerfile.data:
            challenge.dockerfile_filename = form.dockerfile.data.filename
            challenge.dockerfile_data = form.dockerfile.data.read()

        db.session.add(challenge)
        db.session.commit()
        flash("Your challenge has been created!", "success")
        return redirect(url_for("challenges.challenge", challenge_id=challenge.id))
    return render_template(
        "challenges/challenge_add.html",
        title="New Challenge",
        form=form,
        legend="New Challenge",
        challenge=challenge,
    )


@challenges.route("/challenge/<int:challenge_id>")
@login_required
def challenge(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    return render_template(
        "challenges/challenge.html", title=challenge.title, challenge=challenge
    )


@challenges.route("/challenge_download/<challenge_id>/<filetype>")
def download(challenge_id, filetype):
    challenge = Challenge.query.get_or_404(challenge_id)
    if filetype == "supportzip":
        return send_file(
            BytesIO(challenge.supportzip_data),
            attachment_filename=challenge.supportzip_filename,
            as_attachment=True,
        )
    if filetype == "code_scorer":
        return send_file(
            BytesIO(challenge.code_scorer_data),
            attachment_filename=challenge.code_scorer_filename,
            as_attachment=True,
        )
    if filetype == "dockerfile":
        return send_file(
            BytesIO(challenge.dockerfile_data),
            attachment_filename=challenge.dockerfile_filename,
            as_attachment=True,
        )


@challenges.route("/challenges_table")
def challenges_table():
    challenges = Challenge.query
    return render_template(
        "challenges/challenges_table.html",
        title="Challenges Table",
        challenges=challenges,
    )


@challenges.route("/challenge/<int:challenge_id>/update", methods=["GET", "POST"])
@login_required
def update_challenge(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    if current_user.user_role.id != 3 or current_user.id != challenge.user_id:
        abort(403)
    form = ChallengeFormUpdate()
    if form.validate_on_submit():
        challenge.title = form.title.data
        challenge.description = form.description.data
        if form.supportzip.data:
            challenge.supportzip_filename = form.supportzip.data.filename
            challenge.supportzip_data = form.supportzip.data.read()
        if form.code_scorer.data:
            challenge.code_scorer_filename = form.code_scorer.data.filename
            challenge.code_scorer_data = form.code_scorer.data.read()
        if form.dockerfile.data:
            challenge.dockerfile_filename = form.dockerfile.data.filename
            challenge.dockerfile_data = form.dockerfile.data.read()

        db.session.commit()
        flash("Your challenge has been updated!", "success")
        return redirect(url_for("challenges.challenge", challenge_id=challenge.id))
    elif request.method == "GET":
        form.title.data = challenge.title
        form.description.data = challenge.description

    return render_template(
        "challenges/challenge_add.html",
        title="Update Challenge",
        form=form,
        legend="Update Challenge",
        challenge=challenge,
    )


@challenges.route("/challenge/<int:challenge_id>/delete", methods=["POST"])
@login_required
def delete_challenge(challenge_id):
    if current_user.user_role.id != 3:
        abort(403)
    challenge = Challenge.query.get_or_404(challenge_id)
    db.session.delete(challenge)
    db.session.commit()
    flash("Your challenge has been deleted!", "success")
    return redirect(url_for("challenges.challenges_table"))
