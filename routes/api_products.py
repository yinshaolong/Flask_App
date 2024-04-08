from flask import Blueprint, jsonify, request
from db import db
from models import Product
# Creates a Blueprint object (similar to Flask). Make sure you give it a name!
api_products_bp = Blueprint("api_products", __name__)

@api_products_bp.route("/", methods=["GET"])
def api_product_list():
    statement = db.select(Product).order_by(Product.id)
    results = db.session.execute(statement).scalars()
    products = []

    for product in results:
        products.append(product.to_dict())

    return jsonify(products)


@api_products_bp.route("/<int:product_id>", methods=["GET"])
def product_detail_json(product_id):
    product = db.get_or_404(Product, product_id)
    json_record = product.to_dict()
    return jsonify(json_record)

def contains_letter(letter):
    return any(char.isalpha() for char in letter) # ^ "" ^ if is a letter

@api_products_bp.route("/", methods=["POST"])
def product_create():
    print(request.json)
    if "name" not in request.json or "price" not in request.json:
        return jsonify({"error": "Name and price are required"}, 404)
    if not isinstance(request.json["name"], str) or not contains_letter(request.json["name"]) or len(request.json["name"]) < 1: #some products have numbers in their name no-> contains_digit(request.json["name"])
        return jsonify({"error": "Invalid name"}, 400)
    if not isinstance(request.json["price"], float) or request.json["price"] < 0:
        return jsonify({"error": "Invalid price"}, 400)
    product = Product(**request.json)
    db.session.add(product)
    db.session.commit()
    return (jsonify({"Message": "created"}), 201)

@api_products_bp.route("/<int:product_id>", methods=["PUT"])
def product_update(product_id):
    print(request.json)
    possible_keys = ['name', 'price', 'available']
    product = db.get_or_404(Product, product_id)
    if not any(key in request.json for key in possible_keys):
        return jsonify({"error": "Invalid input"}, 400)
    for key in possible_keys:
        if key in request.json:
            # product.key = request.json[key] #this will not work -> must use setattr
            setattr(product, key, request.json[key])
    db.session.commit()
    return (jsonify({"Message": "product updated"}), 204)

@api_products_bp.route("/<int:product_id>", methods=["DELETE"])
def product_delete(product_id):
    product = db.get_or_404(Product, product_id) #session.execute(db.select(Product).where(Product.id == product_id)).scalar() + return 404
    db.session.delete(product)
    db.session.commit()
    return (jsonify({"product deleted"}), 204)