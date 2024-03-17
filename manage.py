import csv
from db import db
from app import app
from models import Customer, Product

def drop_tables():
    db.drop_all()

def create_tables():
    db.create_all()


def seed_database(filename, class_name):
    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            obj = class_name(**row)
            db.session.add(obj)
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        drop_tables()
        create_tables()
        # seed_customers()
        # seed_products()
        seed_database("data/customers.csv", Customer)
        seed_database("data/products.csv", Product)

        
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