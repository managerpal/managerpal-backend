import pytest
import os
from flask import Flask
from flask.testing import FlaskClient


# Import the app factory function
from appcore.app import create_app, db


@pytest.fixture
def app():
    # Create a test app instance using the app factory
    app = create_app(True, "sqlite:///test.db")

    # Configure SQLite test database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()

    yield app

    # Clean up the test database
    os.remove("test.db")


@pytest.fixture
def client(app):
    # Create a test client using Flask's testing framework
    client = app.test_client()
    yield client


def test_signup_and_login(client):
    # Test the first endpoint
    data = {"email": "test@test.com", "username": "user1", "password": "password"}
    response = client.post("/auth/signup", json=data)
    print(response.data)
    assert response.status_code == 200
    response = client.post("/auth/login", json=data)
    assert response.status_code == 200


def test_signup_same_email(client):
    # Test the first endpoint
    response = client.get("/auth/signup")
    assert response.status_code == 200
    response = client.get("/auth/signup")
    assert response.status_code == 400


def test_signup_and_login_wrong_password(client):
    # Test the first endpoint
    response = client.get("/auth/signup")
    assert response.status_code == 200
    response = client.get("/auth/login")
    assert response.status_code == 400


def test_endpoint2(client):
    # Test the second endpoint
    response = client.post("/endpoint2", json={"key": "value"})
    assert response.status_code == 201
    # Add more assertions for the response data if needed
