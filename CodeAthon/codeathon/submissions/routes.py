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
from codeathon.models import Challenge, Contest, Language, Submission, User


submissions = Blueprint("submissions", __name__)


@submissions.route("/submissions_table")
def submissions_table():
    submissions = Submission.query
    return render_template(
        "submissions/submissions_table.html",
        title="Submissions Table",
        submissions=submissions,
    )


@submissions.route("/submission/new", methods=["GET", "POST"])
@login_required
def submission_new():
    form = SubmissionForm()
    form.challenge.choices = [
        (challenge.id, challenge.title)
        for challenge in Challenge.query.order_by(Challenge.title.asc()).all()
    ]
    form.language.choices = [
        (language.id, language.name)
        for language in Language.query.order_by(Language.name.asc()).all()
    ]
    contest = Contest.query.filter_by(active=True).first()
    submission = Submission()
    if form.validate_on_submit():
        submission = Submission(
            language_id=form.language.data,
            user_id=current_user.id,
            contest_id=contest.id,
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
        title="New Submission",
        form=form,
        legend="New Submission",
        submission=submission,
    )


@submissions.route("/submission/<int:submission_id>")
@login_required
def submission(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    title = "Submission"
    return render_template(
        "submissions/submission.html", title=title, submission=submission
    )


@submissions.route("/submission_download/<submission_id>/<filetype>")
def download(submission_id, filetype):
    submission = Submission.query.get_or_404(submission_id)
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

        # <a class="btn btn-secondary btn-sm mt-1 mb-1" href="{{ url_for('submissions.update_submission', submission_id=submission.id) }}">Update</a>
        # <div>
    #    <button type="button" class="btn btn-danger btn-sm m-1" data-bs-toggle="modal" data-bs-target="#deleteModal">Delete</button>
    # </div>
