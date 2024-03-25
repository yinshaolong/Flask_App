from pathlib import Path
from db import db
from flask import Flask, render_template, request, jsonify
import csv
from models import Customer, Product, Order, ProductOrder
app = Flask(__name__)
#this will make flask use a 'sqlite database witht the filename provided
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///store.db"
#this will make flask store the database file inthe path provided
#use "." for the instance path
app.instance_path = Path(".").resolve()
#connects db object with the app object - line 5
db.init_app(app)



@app.route("/")
def home():
    return render_template("base.html")

@app.route("/customers")
def customers():
    statement = db.select(Customer).order_by(Customer.id)
    records = db.session.execute(statement)
    results = records.scalars() #converts into a list
    return render_template("customers.html", customers=results)
           
@app.route("/products")
def products():
    statement = db.select(Product).order_by(Product.id)
    records = db.session.execute(statement)
    results = records.scalars()
    return render_template("products.html", products=results)

@app.route("/customers/<int:customer_id>")
def customer_detail(customer_id):
    # print("in customer details")
    # statement = db.select(Customer).where(Customer.id == customer_id)
    # result = db.session.execute(statement)
    # customer = result.scalar()
    customer = db.get_or_404(Customer, customer_id) #does the same thing as line above, but also returns the 404 error if not found
    return render_template("customer_detail.html", customer=customer)

@app.route("/orders")
def orders():
    statement = db.select(Order).order_by(Order.id)
    records = db.session.execute(statement)
    results = records.scalars()
    return render_template("orders.html", orders=results)



@app.route("/api/customers")
def customers_json():
    statement = db.select(Customer).order_by(Customer.name)
    results = db.session.execute(statement)
    customers = [] #output variable
    for customer in results.scalars(): #scalars is an iterator queue
        json_record = {
            "id": customer.id,
            "name": customer.name,
            "phone": customer.phone,
            "balance": customer.balance
        }
        customers.append(json_record)
    return jsonify(customers)

@app.route("/api/customers/<int:customer_id>")
def customer_detail_json(customer_id):
    # statement = db.select(Customer).where(Customer.id == customer_id)
    # result = db.session.execute(statement)
    # customer = result.scalar()
    customer = db.get_or_404(Customer, customer_id) #does the same thing as line above, but also returns the 404 error if not found
    #single entry so no need to iterate
    json_record = {
            "id": customer.id,
            "name": customer.name,
            "phone": customer.phone,
            "balance": customer.balance
    }
    return jsonify(json_record)

@app.route("/api/customers/<int:customer_id>", methods=["DELETE"])
def customer_delete(customer_id):
    # customer = db.session.execute(db.select(Customer).where(Customer.id == customer_id)).scalar()
    customer = db.get_or_404(Customer, customer_id) #does the same thing as line above, but also returns the 404 error if not found
    db.session.delete(customer)
    db.session.commit()
    return ("deleted", 204)

def contains_digit(number):
    return any(char.isdigit() for char in number) #returns true if ANY character in the string is a digit

def contains_letter(letter):
    return any(char.isalpha() for char in letter) # ^ "" ^ if is a letter

def is_valid_phone(number):
    return len([char for char in number if char.isdigit()]) == 10 #returns true if the length of the list of digits in the string is 10

@app.route("/api/customers", methods=["POST"])
def customer_create():
    print(request.json)
    if "name" not in request.json or "phone" not in request.json:
        return (jsonify({"error": "Name and phone are required"}), 400)
    if isinstance(request.json["name"], str) or contains_digit(request.json["name"]) or len(request.json["name"]) < 1:
        return (jsonify({"error": "Invalid name"}), 400)
    if contains_letter(request.json["phone"]) or not isinstance(request.json["phone"], str) or not is_valid_phone(request.json["phone"]):
        return (jsonify({"error": "Invalid phone number"}), 400)
    customer = Customer(**request.json)
    db.session.add(customer)
    db.session.commit()
    message = "Created"
    return (jsonify({"Message": "created"}), 201)
    # return ("created", 201)

@app.route("/api/customers/<int:customer_id>", methods=["PUT"])
def customer_update(customer_id):
    print(request.json) #requests = balance
    customer = db.get_or_404(Customer, customer_id)
    if 'balance' not in request.json or not isinstance(request.json['balance'], (int, float)):
        return jsonify({"error": "Invalid balance input"}, 400)
    customer.balance = request.json['balance']
    db.session.commit()
    return (jsonify(), 204) #returns an empty json object with a status code of 204

@app.route("/api/products", methods=["POST"])
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

@app.route("/api/products/<int:product_id>", methods=["PUT"])
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

@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def product_delete(product_id):
    product = db.get_or_404(Product, product_id) #session.execute(db.select(Product).where(Product.id == product_id)).scalar() + return 404
    db.session.delete(product)
    db.session.commit()
    return (jsonify({"product deleted"}), 204)
    
@app.route("/api/orders", methods=["POST"])
def order_create():
    print(request.json)
    if "customer_id" not in request.json:
        return jsonify({"error": "Customer ID is required"}, 404)
    if "items" not in request.json or len(request.json["items"]) < 1:
        return jsonify({"error": "Items are required"}, 404)
    order = db.get_or_404(Order, request.json["customer_id"])
    is_valid_order = False
    for item in request.json["items"]:
        if "name" not in item or "quantity" not in item:
            return jsonify({"error": "Product name and quantity are required for each item"}, 404)
        product_statement = db.select(Product).where(Product.name == item["name"])
        product = db.session.execute(product_statement).scalar()
        if product:
            is_valid_order = True
            product_order = ProductOrder(order=order, product=product, quantity=item["quantity"])
            db.session.add(product_order)
            db.session.commit()
    if not is_valid_order:
        return jsonify({"error": "No valid products in the order"}, 404)
    return jsonify({"Message": "Order created"}, 201)

if __name__ == "__main__":
    app.run(debug=True, port=8888)