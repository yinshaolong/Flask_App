from flask import Blueprint, jsonify, request
from sqlalchemy.sql import func
from db import db
from models import Order, Product, ProductOrder, Customer
# Creates a Blueprint object (similar to Flask). Make sure you give it a name!
api_orders_bp = Blueprint("api_orders", __name__)

@api_orders_bp.route("/", methods=["GET"])
def orders_json():
    statement = db.select(Order).order_by(Order.id)
    results = db.session.execute(statement)
    orders = []
    for order in results.scalars():
        json_record = order.to_dict()
        orders.append(json_record)
    return jsonify(orders)



@api_orders_bp.route("/", methods=["POST"])
def order_create():
    print(request.json)
    if "customer_id" not in request.json:
        return jsonify({"error": "valid Customer ID is required"}, 400)
    if "items" not in request.json or len(request.json["items"]) < 1: 
        return jsonify({"error": "Items are required"}, 400)
    customer = db.get_or_404(Customer, request.json["customer_id"])
    is_valid_order = False
    order = Order(customer=customer, created=func.now())
    for item in request.json["items"]:
        if "name" not in item or "quantity" not in item:
            return jsonify({"error": "Product name and quantity are required for each item"}, 404)
        product_statement = db.select(Product).where(Product.name == item["name"])
        product = db.session.execute(product_statement).scalar()
        if product:
            is_valid_order = True
            if not isinstance(item["quantity"], int) or item["quantity"] < 1:
                return jsonify({"error": "Invalid quantity"}, 404)
            product_order = ProductOrder(order=order, product=product, quantity=item["quantity"])
            db.session.add(product_order)
            db.session.commit()
    if not is_valid_order:
        return jsonify({"error": "No valid products in the order"}, 404)
    return jsonify({"Message": "Order created"}, 201)



@api_orders_bp.route("/<int:order_id>", methods=["PUT"])
def process_order(order_id):
    print("this is request", request.json)
    if "processed" not in request.json or not isinstance(request.json["processed"], bool):
        return jsonify({"error": "missing viable'processed' key"}, 404)
    
    if not request.json["processed"]: #if processed is false
        return jsonify({"error": "process not yet completed"}, 404)
    
    strategy = "adjust" #default
    if "strategy" in request.json:
        if request.json["strategy"] in ["adjust", "reject", "ignore"]:
            strategy = request.json["strategy"]
        else:
            return jsonify({"error": "Invalid strategy"}, 404)
        
    order = db.get_or_404(Order, order_id)
    process = order.process_order(strategy)
    if not process:
        return jsonify({"error": "Order not processed"}, 404)
    db.session.commit()
    return jsonify({"Message": f"Strategy: {strategy} - Order processed "}, 204)