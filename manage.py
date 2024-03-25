import csv
from db import db
from app import app
from models import Customer, Product, Order, ProductOrder
from sqlalchemy import func
import random

def drop_tables():
    db.drop_all()

def create_tables():
    db.create_all()

def randomize_orders():
    cust_statement = db.select(Customer).order_by(func.random()).limit(1)
    customer = db.session.execute(cust_statement).scalar()
    # Make an order
    order = Order(customer=customer) #order only takes one argument, customer
    db.session.add(order)
    # Find a random product
    prod_statement = db.select(Product).order_by(func.random()).limit(1)
    product = db.session.execute(prod_statement).scalar()
    rand_qty = random.randint(10, 20)
    # Add that product to the order
    association_1 = ProductOrder(order=order, product=product, quantity=rand_qty)
    db.session.add(association_1)
    # Do it again
    prod_statement = db.select(Product).order_by(func.random()).limit(1)
    product = db.session.execute(prod_statement).scalar()
    rand_qty = random.randint(10, 20)
    association_2 = ProductOrder(order=order, product=product, quantity=rand_qty)
    db.session.add(association_2)
    # Commit to the database
    db.session.commit()


def seed_database(filename, class_type):
    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            obj = class_type(**row)
            db.session.add(obj)
        db.session.commit()

if __name__ == "__main__":
    with app.app_context(): #makes the application instance and other context variables accessible
        drop_tables()
        create_tables()
        seed_database("data/customers.csv", Customer)
        seed_database("data/products.csv", Product)
        for _ in range(10):
            randomize_orders()

        # seed_customers()
        # seed_products()


# def seed_customers():
#     with open('data/customers.csv', 'r') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             customer = Customer(name = row['name'], phone = row['phone'], balance = 0)
#             db.session.add(customer)
#         db.session.commit()

# def seed_products():
#     with open('data/products.csv', 'r') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             product = Product(name = row['name'], price = row['price'])
#             db.session.add(product)
#         db.session.commit()