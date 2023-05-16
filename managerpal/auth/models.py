from appcore.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    name = Column(String(1000))
    updates = relationship("Update", backref="user")
    tokens = relationship("SecurityToken", backref="user")

class JWT(Base):
    """
    Store JWT to allow for authenticated QR code links
    """
    __tablename__ ="jwt"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    token = Column()