import pytest
from flask import Flask
from flask.testing import FlaskClient


# Import the app factory function
from appcore.app import create_app, db

AUTH_DATA = {
    "email": "testinventory@test.com",
    "username": "userinv",
    "password": "password",
}


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


def create_acc_to_test(client):
    # Test the first endpoint
    response = client.post("/auth/signup", json=AUTH_DATA)
    assert response.status_code == 200
    response = client.post("/auth/login", json=AUTH_DATA)
    assert response.status_code == 200


def test_create_product_and_get_product(client):
    response = client.post("/auth/signup", json=AUTH_DATA)
    response = client.post("/auth/login", json=AUTH_DATA)
    response = client.post("/auth/login", json=AUTH_DATA)
    data = {
        "name": "Logitech G402",
        "action": "Buy",
        "date": "2023-06-25",
        "price": "100.00",
        "sku": "1jad81h419sk",
    }
    response = client.post("/inventory/add_product", json=data)
    assert response.status_code == 200
    response = client.get("/inventory/list_products")
    assert response.status_code == 200
    assert response.get_json() == {
        "items": [
            {"id": 1, "name": "Logitech G402", "qty": None, "sku": "1jad81h419sk"}
        ]
    }


def test_create_update_and_list_updates(client):
    response = client.post("/auth/signup", json=AUTH_DATA)
    response = client.post("/auth/login", json=AUTH_DATA)
    response = client.post("/auth/login", json=AUTH_DATA)
    response = client.get("/inventory/list_products")
    assert response.status_code == 200
    assert response.get_json() == {
        "items": [
            {"id": 1, "name": "Logitech G402", "qty": None, "sku": "1jad81h419sk"}
        ]
    }
    data = {
        "product_id": 1,
        "action": "buy",
        "price": 100,
        "arrived": False,
        "quantity": 500,
        "date": "2023-07-23",
    }
    response = client.post("/inventory/update", json=data)
    assert response.status_code == 200
