import datetime
from flask import Blueprint, jsonify, request
from flask_login import login_required
from inventory.models import Product, Item, Update

from appcore.db import db

inventory_bp = Blueprint("inventory", __name__)


@login_required
@inventory_bp.route("/list")
def list_inventory():
    all_products = Product.query.all()
    ret = {"items": []}
    for product in all_products:
        item = {}
        item["id"] = product.id
        item["name"] = product.name
        item["qty"] = product.quantity
        ret["items"].append(item)

    return jsonify(ret)


@login_required
@inventory_bp.route("/add_product", methods=["POST"])
def add_product():
    data = request.form
    try:
        name = data.get("name")
        quantity = data.get("quantity", None)
    except ValueError as ve:
        return (
            jsonify({"success": False, "error": f"'name' is missing from request"}),
            400,
            {"ContentType": "application/json"},
        )
    pd = Product(name=name, quantity=quantity)
    db.session.add(pd)
    db.session.commit()
    return (
        jsonify({"success": True, "error": None}),
        200,
        {"ContentType": "application/json"},
    )


@login_required
@inventory_bp.route("/update", methods=["POST"])
def update():
    data = request.form
    try:
        product_id = data.get("product_id")
        update_type = data.get("action")
        price = data.get("price", None)
        arrived = data.get("arrived", True)
        quantity = data.get("quantity")
        date = data.get("date")
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError as ve:
        return (
            jsonify({"success": False, "error": f"{ve}"}),
            400,
            {"ContentType": "application/json"},
        )
    all_products = Product.query.filter_by(id=product_id).first()
    if not all_products:
        return (
            jsonify(
                {
                    "success": False,
                    "error": f"Product with ID {product_id} does not exist!",
                }
            ),
            400,
            {"ContentType": "application/json"},
        )
    if arrived:
        if update_type.lower() == "buy":
            arrived = False
    ud = Update(
        product_id=product_id,
        price=price,
        quantity=quantity,
        date=date,
        arrived=arrived,
        update_type=update_type,
    )
    db.session.add(ud)
    db.session.commit()
    return (
        jsonify({"success": True, "error": None}),
        200,
        {"ContentType": "application/json"},
    )


@login_required
@inventory_bp.route("/arriving", methods=["GET", "POST"])
def arriving():
    print(request.method)
    data = request.form
    try:
        product_id = data.get("product_id", None)
        if request.method == "POST":
            update_id = data.get("id")
    except ValueError as ve:
        return (
            jsonify({"success": False, "error": f"{ve}"}),
            400,
            {"ContentType": "application/json"},
        )
    if request.method == "GET":
        if product_id:
            arriving_products = Update.query.filter(
                arriving=False, product_id=product_id
            )
        else:
            arriving_products = Update.query.all()
        ret = {"items": []}
        for product in arriving_products:
            item = {}
            item["id"] = product.id
            item["qty"] = product.quantity
            ret["items"].append(item)
        return (
            jsonify(ret),
            200,
            {"ContentType": "application/json"},
        )
    elif request.method == "POST":
        arriving_product = Update.query.filter(id=update_id)
        if not arriving_product:
            return (
                jsonify({"success": False, "error": "No product with that ID"}),
                400,
                {"ContentType": "application/json"},
            )
        arriving_product.arrived = True
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
