import os

from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

import appcore.config as config
from appcore.db import db

# Import blueprints
from auth.views import auth_bp
from auth.models import User
from inventory.views import inventory_bp


def create_app(test: bool = False, temp_sqlite_uri: str = None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI

    app.config["SECRET_KEY"] = config.SECRET_KEY
    if os.environ.get("is_dev", False) or app.config["TESTING"] or test:
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
            basedir, "database.db" if not temp_sqlite_uri else temp_sqlite_uri
        )
        app.config["SECRET_KEY"] = "asdas123asdasd"
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    CORS(app)

    return app
