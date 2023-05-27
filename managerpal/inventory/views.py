from flask import Blueprint, jsonify
from inventory.models import Product, Item, Update

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.route("/list")
def list_inventory():
    all_products = Product.query.all()
    return jsonify(all_products)
