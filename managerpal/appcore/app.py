import sqlalchemy

from flask import Flask, g
from flask_cors import CORS

import appcore.config as config
from appcore.db import db

# Import blueprints
from auth.views import auth_bp
from inventory.views import inventory_bp


def register_hooks(app, db):
    """
    Inspiration from https://github.com/alexferl/flask-simpleldap/blob/master/examples/blueprints/blueprints/app.py
    Just need the before_request to dispose of the previous engine
    to prevent two subprocesses from trying to access the same
    db session
    """

    @app.before_request
    def before_request():
        """
        https://stackoverflow.com/questions/66876181/how-do-i-close-a-flask-sqlalchemy-connection-that-i-used-in-a-thread
        """
        db.get_engine(app).dispose()
        g.db = db

    @app.teardown_request
    def shutdown_session(exception=None):
        """
        https://stackoverflow.com/questions/28168554/flask-sqlalchemy-and-sqlalchemy
        """
        g.db.session.remove()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI

    db.init_app(app)

    # register_hooks(app, db)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    CORS(app)

    return app