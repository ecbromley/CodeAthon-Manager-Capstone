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
from codeathon import db
from codeathon.submissions.forms import SubmissionForm
from codeathon.models import Contest, Submission, User


submissions = Blueprint("submissions", __name__)


@submissions.route("/submissions_table")
def submissions_table():
    submissions = Submission.query
    return render_template(
        "submissions/submissions_table.html",
        title="submissions Table",
        submissions=submissions,
    )


@submissions.route("/submission/new", methods=["GET", "POST"])
@login_required
def submission_new():
    form = SubmissionForm()
    submission = Submission()
    if form.validate_on_submit():
        submission = submission(
            language_id=form.language.data,
            user_id=current_user.id,
            contest_id=Contest.query.filter_by(active=True).first(),
            challenge_id=form.challenge.data,
        )
        if form.code.data:
            submission.code_filename = form.code.data.filename
            submission.code_data = form.code.data.read()
        if form.code_output.data:
            submission.code_output_filename = form.code_output.data.filename
            submission.code_output_data = form.code_output.data.read()

        db.session.add(submission)
        db.session.commit()
        flash("Your solution has been submitted!", "success")
        return redirect(url_for("submissions.submission", submission_id=submission.id))
    return render_template(
        "submissions/submission_add.html",
        title="New submission",
        form=form,
        legend="New submission",
        submission=submission,
    )


@submissions.route("/submission/<int:submission_id>")
@login_required
def submission(submission_id):
    submission = submission.query.get_or_404(submission_id)
    return render_template(
        "submissions/submission.html", title=submission.title, submission=submission
    )


@submissions.route("/submission_download/<submission_id>/<filetype>")
def download(submission_id, filetype):
    submission = submission.query.get_or_404(submission_id)
    if filetype == "code":
        return send_file(
            BytesIO(submission.code_data),
            attachment_filename=submission.code_filename,
            as_attachment=True,
        )
    if filetype == "code_output":
        return send_file(
            BytesIO(submission.code_output_data),
            attachment_filename=submission.code_output_filename,
            as_attachment=True,
        )
