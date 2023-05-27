from appcore.db import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    name = Column(String(1000))
    is_active = Column(Boolean)
    is_anonymous = Column(Boolean)
    is_authenticated = Column(Boolean)

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
