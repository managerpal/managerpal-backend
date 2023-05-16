from flask import Blueprint, jsonify
from inventory.models import Product, Item, Update

inventory = Blueprint('inventory', __name__)

@inventory.route('/list')
def list_inventory():
    all_products = Product.query.all()
    return jsonify(all_products.dumps())