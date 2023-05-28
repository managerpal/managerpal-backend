import os

from sqlalchemy.engine.url import URL

APP_PORT = 5000
SECRET_KEY = os.environ.get("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = URL.create(
    drivername="postgresql",
    username="managerpal",
    password="managerpal",
    host="backend-db",
    database="managerpal",
)
