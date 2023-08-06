import pytest


# Import the app factory function
from appcore.app import create_app, db


@pytest.fixture
def app():
    # Create a test app instance using the app factory
    app = create_app()
    # app = create_app(True, "sqlite:///test.db")

    # Configure SQLite test database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture
def client(app):
    # Create a test client using Flask's testing framework
    client = app.test_client()
    yield client


def test_signup_and_login(client):
    data = {"email": "test@test.com", "username": "user1", "password": "password"}
    response = client.post("/auth/signup", json=data)
    assert response.status_code == 200
    response = client.post("/auth/login", json=data)
    assert response.status_code == 200


def test_signup_same_email(client):
    data = {"email": "test2@test.com", "username": "user2", "password": "password"}
    response = client.post("/auth/signup", json=data)
    assert response.status_code == 200
    data = {"email": "test2@test.com", "username": "user2", "password": "password"}
    response = client.post("/auth/signup", json=data)
    assert response.status_code == 400


def test_signup_and_login_wrong_password(client):
    data = {"email": "test3@test.com", "username": "user3", "password": "password"}
    response = client.post("/auth/signup", json=data)
    assert response.status_code == 200
    data = {"email": "test3@test.com", "username": "user3", "password": "wrongpassword"}
    response = client.post("/auth/login", json=data)
    assert response.status_code == 400


def test_signup_and_login_and_logout_unauth(client):
    data = {"email": "test4@test.com", "username": "user4", "password": "password"}
    response = client.post("/auth/signup", json=data)
    assert response.status_code == 200
    response = client.post("/auth/login", json=data)
    assert response.status_code == 200
    response = client.get("/auth/logout", json=data)
    assert response.status_code == 200
