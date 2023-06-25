import json

from flask import Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from appcore.db import db
from auth.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    email = data.get("email")
    email = email.lower()
    password = data.get("password")
    remember = True if data.get("remember") else False

    user = db.session.query(User).filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        return json.dumps({"success": False}), 400, {"ContentType": "application/json"}

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@auth_bp.route("/signup", methods=["POST"])
def signup():
    # Workaround to accept both application/json and multipart data
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    email = data.get("email")
    email = email.lower()
    name = data.get("name")
    password = data.get("password")

    user = (
        db.session.query(User).filter_by(email=email).first()
    )  # if this returns a user, then the email already exists in database

    if (
        user
    ):  # if a user is found, we want to redirect back to signup page so user can try again
        return (
            json.dumps({"success": False, "error": "Email already exists"}),
            400,
            {"ContentType": "application/json"},
        )

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method="scrypt"),
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}
