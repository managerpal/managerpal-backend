from appcore.db import db


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False, comment="Name of item")
    price = db.Column(db.Float, nullable=True, comment="Price of item")


class Item(db.Model):
    __tablename__ = "item"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    product_id = db.relationship("Product", foreign_keys="Item.product_id")
