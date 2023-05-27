import datetime

from appcore.db import db
from sqlalchemy import DateTime, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Product(db.Model):
    __tablename__ = "product"

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False, comment="Name of item")
    price = Column(Float, nullable=True, comment="Price of item")  # Might not be using
    quantity = Column(Integer, nullable=True, comment="Quantity of item left")
    updates = relationship("Update", backref="product_rls")


class Item(db.Model):
    __tablename__ = "item"

    id = Column(Integer, nullable=False, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"))


class Update(db.Model):
    __tablename__ = "update"

    id = Column(Integer, nullable=False, primary_key=True)
    quantity = Column(
        Integer, nullable=False, comment="Quantity of items added or removed"
    )
    product_id = Column(Integer, ForeignKey("product.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    date = Column(DateTime, default=datetime.datetime.utcnow)
