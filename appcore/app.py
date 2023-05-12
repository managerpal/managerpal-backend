import sqlalchemy

from flask import Flask, g

from appcore import db

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    db.init_app(app)


    return app
