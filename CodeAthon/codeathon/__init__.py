from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from codeathon.config import Config
from sqlalchemy import MetaData

db = SQLAlchemy(
    metadata=MetaData(
        naming_convention={
            "pk": "pk_%(table_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "ix": "ix_%(table_name)s_%(column_0_name)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
        }
    )
)
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from codeathon.admin.routes import admin
    from codeathon.challenges.routes import challenges
    from codeathon.errors.handlers import errors
    from codeathon.main.routes import main
    from codeathon.posts.routes import posts
    from codeathon.users.routes import users

    app.register_blueprint(admin)
    app.register_blueprint(challenges)
    app.register_blueprint(errors)
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(users)

    return app
