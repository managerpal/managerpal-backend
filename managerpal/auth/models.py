from appcore.db import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    name = Column(String(1000))
    updates = relationship("Update", back_populates="user_rls")
    tokens = relationship("SecurityToken", back_populates="user_rls")


class JWT(db.Model):
    """
    Store JWT to allow for authenticated QR code links
    """

    __tablename__ = "jwt"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    token = Column()
