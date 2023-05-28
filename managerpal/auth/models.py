from appcore.db import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))
    name = db.Column(db.String(1000))

    updates = relationship("Update", back_populates="user_rls")
    # tokens = relationship("jwt", back_populates="user")


# class JWT(db.Model):
#     """
#     Store JWT to allow for authenticated QR code links
#     """

#     __tablename__ = "jwt"

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("user.id"))
#     # token = Column()

#     user = relationship("User", back_populates="tokens")
