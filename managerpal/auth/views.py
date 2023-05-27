from flask import Blueprint
from appcore.db import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login")
def login():
    return "Login"


@auth_bp.route("/signup")
def signup():
    return "Signup"


@auth_bp.route("/logout")
def logout():
    return "Logout"
