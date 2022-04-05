from datetime import datetime

# import imp
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from codeathon import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    support_zip_file = db.Column(db.LargeBinary, nullable=True)
    code_scoring = db.Column(db.LargeBinary, nullable=True)
    dockerfile = db.Column(db.LargeBinary, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    submissions = db.relationship(
        "Submission", backref="submission_challenge", lazy=True
    )


challenges = db.Table(
    "contest_challenges",
    db.Column("contest_id", db.Integer, db.ForeignKey("contest.id")),
    db.Column("challenge_id", db.Integer, db.ForeignKey("challenge.id")),
)


class Contest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    submissions = db.relationship("Submission", backref="submission_contest", lazy=True)
    challenges = db.relationship(
        "Challenge", secondary=challenges, backref="challenge_contest", lazy=True
    )


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    submissions = db.relationship(
        "Submission", backref="submission_language", lazy=True
    )


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship("User", backref="user_role", lazy=True)


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_submitted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    code_file = db.Column(db.LargeBinary, nullable=True)
    code_output = db.Column(db.LargeBinary, nullable=True)
    score = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    contest_id = db.Column(db.Integer, db.ForeignKey("contest.id"), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenge.id"), nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey("language.id"), nullable=False)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    users = db.relationship("User", backref="user_team", lazy=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    team = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=True)
    submissions = db.relationship("Submission", backref="submission_author", lazy=True)
    challenges = db.relationship("Challenge", backref="challenge_author", lazy=True)

    def get_reset_token(self):
        s = Serializer(current_app.config["SECRET_KEY"])
        return s.dumps({"user_id": self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token, expires_sec)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
