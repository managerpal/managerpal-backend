import datetime
from flask import Blueprint, jsonify, request
from flask_login import login_required
from inventory.models import Product, Item, Update

from appcore.db import db

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.route("/list")
@login_required
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


@inventory_bp.route("/add_product", methods=["POST"])
@login_required
def add_product():
    if request.is_json:
        data = request.get_json()
    else:
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


@inventory_bp.route("/update", methods=["POST"])
@login_required
def update():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    try:
        product_id = data.get("product_id")
        update_type = data.get("action")
        update_type = update_type.lower()
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
        if update_type == "buy":
            arrived = False
    if update_type == "sell":
        product = Product.query.filter_by(id=product_id).first()
        product.quantity = product.quantity - quantity
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


@inventory_bp.route("/arriving", methods=["GET", "POST"])
@login_required
def arriving():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    try:
        # product_id = data.get("product_id", None)
        product_id = request.args.get("product_id", None)
        if request.method == "POST":
            update_id = data.get("id")
            arrived = data.get("arrived", False)
    except ValueError as ve:
        return (
            jsonify({"success": False, "error": f"{ve}"}),
            400,
            {"ContentType": "application/json"},
        )
    if request.method == "GET":
        if product_id:
            arriving_updates = Update.query.filter_by(
                arrived=False, product_id=product_id
            )
        else:
            arriving_updates = Update.query.filter_by(arrived=False)
        ret = {"items": []}
        for update in arriving_updates:
            item = {}
            item["product_id"] = update.product_id
            item["product_name"] = update.product_rls.name
            item["id"] = update.id
            item["date"] = update.date
            item["qty"] = update.quantity
            ret["items"].append(item)
        return (
            jsonify(ret),
            200,
            {"ContentType": "application/json"},
        )
    elif request.method == "POST":
        arriving_updates = Update.query.filter_by(id=update_id).first()
        if not arriving_updates:
            return (
                jsonify({"success": False, "error": "No product with that ID"}),
                400,
                {"ContentType": "application/json"},
            )
        # Silently disallow updating to the same arriving
        if arriving_updates.arrived != arrived:
            arriving_updates.arrived = arrived
            arriving_product = arriving_updates.product_rls
            if not arriving_product.quantity:
                if arrived:
                    arriving_product.quantity = arriving_updates.quantity
                else:
                    arriving_product.quantity = 0
            else:
                if arrived:
                    arriving_product.quantity = (
                        arriving_product.quantity + arriving_updates.quantity
                    )
                else:
                    arriving_product.quantity = (
                        arriving_product.quantity - arriving_updates.quantity
                    )
            db.session.commit()
        return (
            jsonify({"success": True, "error": None}),
            200,
            {"ContentType": "application/json"},
        )


@inventory_bp.route("/add_item", methods=["POST"])
@login_required
def add_items():
    if request.is_json:
        data = request.get_json()
    else:
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
