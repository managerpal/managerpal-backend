import sqlalchemy

from flask import Flask, g
from flask_cors import CORS

import config
from db import db


def register_hooks(app):
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
    register_hooks(app)
    CORS(app)

    return app
