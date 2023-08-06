import pytest


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
    response = client.get("/inventory/list_updates?product_id=1")
    assert response.status_code == 200
    assert response.get_json() == [
        {
            "action": "buy",
            "arrived": False,
            "date": "Sun, 23 Jul 2023 00:00:00 GMT",
            "id": 1,
            "price": 100.0,
            "product_id": 1,
            "qty": 500,
        }
    ]


def test_arriving(client):
    response = client.post("/auth/signup", json=AUTH_DATA)
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
    response = client.get("/inventory/list_updates?product_id=1")
    assert response.status_code == 200
    assert response.get_json() == [
        {
            "action": "buy",
            "arrived": False,
            "date": "Sun, 23 Jul 2023 00:00:00 GMT",
            "id": 1,
            "price": 100.0,
            "product_id": 1,
            "qty": 500,
        },
        {
            "action": "buy",
            "arrived": False,
            "date": "Sun, 23 Jul 2023 00:00:00 GMT",
            "id": 2,
            "price": 100.0,
            "product_id": 1,
            "qty": 500,
        },
    ]
    data = {"id": 1, "arrived": True}
    response = client.post("/inventory/arriving", json=data)
    assert response.status_code == 200
    response = client.get("/inventory/arriving")
    assert response.status_code == 200
    assert response.get_json() == {
        "items": [
            {
                "date": "Sun, 23 Jul 2023 00:00:00 GMT",
                "id": 2,
                "product_id": 1,
                "product_name": "Logitech G402",
                "qty": 500,
            }
        ]
    }


def test_product_detailed_after_selling(client):
    response = client.post("/auth/signup", json=AUTH_DATA)
    response = client.post("/auth/login", json=AUTH_DATA)
    response = client.get("/inventory/list_products")
    assert response.status_code == 200
    data = {
        "product_id": 1,
        "action": "sell",
        "price": 105,
        "arrived": False,
        "quantity": 1000,
        "date": "2023-07-24",
    }
    response = client.post("/inventory/update", json=data)
    assert response.status_code == 200
    response = client.get("/inventory/product_detailed?product_id=1")
    assert response.get_json() == {
        "product_id": "1",
        "profit": 5000.0,
        "total_arrived": 0,
        "total_bought": 1000,
        "total_expense": 100000.0,
        "total_revenue": 105000.0,
        "total_sold": 1000,
    }
