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

'''new code //old commented below'''
@api_products_bp.route("/", methods=["POST"])
def product_create():
    data = request.json
    if "name" not in data or "price" not in data:
        return "Error - invalid keys", 400
    name = data["name"]
    price = data["price"]
    
    if not isinstance(price, (int, float)) or price < 0:
        return "Error - invalid price value", 400
    if not isinstance(name, str) or len(name) < 1 or contains_digit(name):
        return "Error - invalid name", 400
    
    statement = db.select(Product).where(Product.name == name)
    record = db.session.execute(statement).scalar()
    if record:
        return "Error - product already exists", 400
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return f"Product {product.name} Created", 201

def contains_digit(number):
    return any(char.isdigit() for char in number) #returns true if ANY character in the string is a digit
# @api_products_bp.route("/", methods=["POST"])
# def product_create():
#     print(request.json)
#     if "name" not in request.json or "price" not in request.json:
#         return jsonify({"error": "Name and price are required"}, 404)
#     if not isinstance(request.json["name"], str) or not contains_letter(request.json["name"]) or len(request.json["name"]) < 1: #some products have numbers in their name no-> contains_digit(request.json["name"])
#         return jsonify({"error": "Invalid name"}, 400)
#     if not isinstance(request.json["price"], float) or request.json["price"] < 0:
#         return jsonify({"error": "Invalid price"}, 400)
#     product = Product(**request.json)
#     db.session.add(product)
#     db.session.commit()
#     return (jsonify({"Message": "created"}), 201)

@api_products_bp.route("/<int:product_id>", methods=["PUT"])
def product_update(product_id):
    data = request.json
    possible_keys = ['name', 'price', 'available']
    if "name" not in data or "price" not in data or "available" not in data:
        return "Error: keys (name / price / available) are missing", 400
    name = data["name"]
    price = data["price"]
    available = data["available"]

    if not isinstance(price, (int, float)) or price < 0:
        return "Error - invalid price value", 400
    if not isinstance(name, str) or len(name) < 1 or contains_digit(name):
        return "Error - invalid name"
    if not isinstance(available, int) or available < 1:
        return "Error - invalid quantity", 400

    product = db.get_or_404(Product, product_id)
    
    for key in possible_keys:
        if key in data:
            setattr(product, key, data[key])
    db.session.commit()
    return f"Product {product.id}. {product.name} has been updated. Price is ${product.price} and availability is {product.available} "

def contains_digit(number):
    return any(char.isdigit() for char in number) #returns true if ANY character in the string is a digit

# @api_products_bp.route("/<int:product_id>", methods=["PUT"])
# def product_update(product_id):
#     print(request.json)
#     possible_keys = ['name', 'price', 'available']
#     product = db.get_or_404(Product, product_id)
#     if not any(key in request.json for key in possible_keys):
#         return jsonify({"error": "Invalid input"}, 400)
#     for key in possible_keys:
#         if key in request.json:
#             # product.key = request.json[key] #this will not work -> must use setattr
#             setattr(product, key, request.json[key])
#     db.session.commit()
#     return (jsonify({"Message": "product updated"}), 204)

@api_products_bp.route("/<int:product_id>", methods=["DELETE"])
def product_delete(product_id):
    product = db.get_or_404(Product, product_id) #session.execute(db.select(Product).where(Product.id == product_id)).scalar() + return 404
    db.session.delete(product)
    db.session.commit()
    return (jsonify({"product deleted"}), 204)