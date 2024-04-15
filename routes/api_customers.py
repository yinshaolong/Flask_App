from flask import Blueprint, jsonify, request
from db import db
from models import Customer
# Creates a Blueprint object (similar to Flask). Make sure you give it a name!
api_customers_bp = Blueprint("api_customers", __name__)

#automatically appends /api/customers to the route
@api_customers_bp.route("/", methods=["GET"])
def customers_json():
    statement = db.select(Customer).order_by(Customer.name)
    results = db.session.execute(statement)
    customers = [] #output variable
    for customer in results.scalars(): #scalars is an iterator queue
        json_record = customer.to_dict()
        print("json record",type(json_record))
        customers.append(json_record)
    return jsonify(customers)

@api_customers_bp.route("/<int:customer_id>", methods=["GET"])
def customer_detail_json(customer_id):
    # statement = db.select(Customer).where(Customer.id == customer_id)
    # result = db.session.execute(statement)
    # customer = result.scalar()
    customer = db.get_or_404(Customer, customer_id) #does the same thing as line above, but also returns the 404 error if not found
    #single entry so no need to iterate
    json_record = customer.to_dict()
    return jsonify(json_record)

@api_customers_bp.route("/<int:customer_id>", methods=["DELETE"])
def customer_delete(customer_id):
    # customer = db.session.execute(db.select(Customer).where(Customer.id == customer_id)).scalar()
    customer = db.get_or_404(Customer, customer_id) #does the same thing as line above, but also returns the 404 error if not found
    db.session.delete(customer)
    db.session.commit()
    return ("deleted", 204)


'''
new code //old commented below
'''
@api_customers_bp.route("/", methods=["POST"])
def customer_create():
    data = request.json
    if "name" not in data or "phone" not in data:
        return "Invalid request", 400
    
    #checked exist, so can now store in variable
    name = data["name"]
    phone = data["phone"]

    #check if name is unique
    statement = db.select(Customer).where(Customer.name == data["name"])
    result = db.session.execute(statement).scalar()
    if result:
        return "Error: name already exists", 400
    #result not in use, therefore must make customer if all other checks pass
    if name == "" or not isinstance(name, str) or contains_digit(name):
        return "Error: name not valid", 400
    if not isinstance(phone, str) or len(phone) != 12 or not valid_phone_number(phone):
        return "Error: phone not valid", 400
    
    customer = Customer(**data)
    db.session.add(customer)
    db.session.commit()
    return f'Customer {name} created', 201
    



def contains_digit(number):
    return any(char.isdigit() for char in number) #returns true if ANY character in the string is a digit

def contains_two_hyphens(number):
    hypens = 0
    for char in number:
        if char == "-":
            hypens += 1
    return hypens ==2

def valid_phone_number(letter):
    has_letter =  any(char.isalpha() for char in letter) # ^ "" ^ if is a letter
    return contains_two_hyphens(letter) and not has_letter

# def contains_digit(number):
#     return any(char.isdigit() for char in number) #returns true if ANY character in the string is a digit

# def contains_letter(letter):
#     return any(char.isalpha() for char in letter) # ^ "" ^ if is a letter

# def is_valid_phone(number):
#     return len([char for char in number if char.isdigit()]) == 10 #returns true if the length of the list of digits in the string is 10

# def customer_create():
#     print(request.json)
#     if "name" not in request.json or "phone" not in request.json:
#         return (jsonify({"error": "Name and phone are required"}), 400)
#     if isinstance(request.json["name"], str) or contains_digit(request.json["name"]) or len(request.json["name"]) < 1:
#         return (jsonify({"error": "Invalid name"}), 400)
#     if contains_letter(request.json["phone"]) or not isinstance(request.json["phone"], str) or not is_valid_phone(request.json["phone"]):
#         return (jsonify({"error": "Invalid phone number"}), 400)
#     customer = Customer(**request.json)
#     db.session.add(customer)
#     db.session.commit()
#     message = "Created"
#     return (jsonify({"Message": "created"}), 201)
#     # return ("created", 201)

@api_customers_bp.route("/<int:customer_id>", methods=["PUT"])
def customer_update(customer_id):
    print(request.json) #requests = balance
    customer = db.get_or_404(Customer, customer_id)
    if 'balance' not in request.json or not isinstance(request.json['balance'], (int, float)):
        return jsonify({"error": "Invalid balance input"}, 400)
    customer.balance = request.json['balance']
    db.session.commit()
    return (jsonify(customer.to_dict()), 204) 
