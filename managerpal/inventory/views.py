from flask import Blueprint, jsonify, request
from flask_login import login_required
from inventory.models import Product, Item, Update

from appcore.db import db

inventory_bp = Blueprint("inventory", __name__)


@login_required
@inventory_bp.route("/list")
def list_inventory():
    all_products = Product.query.all()
    return jsonify(all_products)


@login_required
@inventory_bp.route("/add_product", methods=["POST"])
def add_product():
    data = request.form
    name = data.get("name")
    price = data.get("price", None)
    quantity = data.get("quantity")

    pd = Product(name, price, quantity)
    db.session.add(pd)
    db.session.commit()
    return (
        jsonify({"success": True, "error": None}),
        200,
        {"ContentType": "application/json"},
    )


@login_required
@inventory_bp.route("/add_item", methods=["POST"])
def add_items():
    data = request.form
    name = data.get("name")
    price = data.get("price", None)
    quantity = data.get("quantity")

    pd = Product(name, price, quantity)
    db.session.add(pd)
    db.session.commit()
    return (
        jsonify({"success": True, "error": None}),
        200,
        {"ContentType": "application/json"},
    )
