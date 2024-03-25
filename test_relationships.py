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

import random
import string

def random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def test_relationships():
    with app.app_context():
        # Create a customer with a random name
        customer = Customer(name=random_string(), phone="1234567890", balance=100.0)
        db.session.add(customer)
        db.session.commit()

        # Create a product with a random name
        product_name = random_string()
        product = Product(name=product_name, price=10.0, available=100)
        db.session.add(product)
        db.session.commit()

        # Create an order for the customer
        order = Order(customer_id=customer.id, total=20.0)
        db.session.add(order)
        db.session.commit()

        # Create a ProductOrder for the order
        product_order = ProductOrder(order_id=order.id, product_id=product.id, quantity=2)
        db.session.add(product_order)
        db.session.commit()

        # Check the relationships
        assert customer.orders == [order]
        assert order.customer == customer
        assert order.items == [product_order]
        assert order.items[0].product == product
        assert order.items[0].product.name == product_name
        assert order.items[0].quantity == 2

        # Clean up
        db.session.delete(product_order)
        db.session.delete(order)
        db.session.delete(product)
        db.session.delete(customer)
        db.session.commit()
