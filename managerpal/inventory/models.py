import datetime

from appcore.db import db
from sqlalchemy import DateTime, Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Product(db.Model):
    __tablename__ = "product"

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False, comment="Name of item")
    price = Column(Float, nullable=True, comment="Price of item")  # Might not be using
    quantity = Column(Integer, nullable=True, comment="Quantity of item left")

    updates = relationship("Update", back_populates="product_rls")
    items = relationship("Item", back_populates="product_rls")


class Item(db.Model):
    __tablename__ = "item"

    id = Column(Integer, nullable=False, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"))

    product_rls = relationship("Product", back_populates="items")


class Update(db.Model):
    __tablename__ = "update"

    id = Column(Integer, nullable=False, primary_key=True)
    update_type = Column(
        String,
        nullable=False,
        comment="Type of update, buy or sell",  # TODO: Add enum
    )
    quantity = Column(
        Integer, nullable=False, comment="Quantity of items added or removed"
    )
    price = Column(Float, nullable=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    arrived = Column(Boolean, nullable=True)

    user_rls = relationship("User", back_populates="updates")
    product_rls = relationship("Product", back_populates="updates")
