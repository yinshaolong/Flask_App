import csv
from db import db
from app import app
from models import Customer  # import your Customer model

def drop_tables():
    with app.app_context():
        db.drop_all()

def create_tables():
    with app.app_context():
        db.create_all()

def seed_database():
    with app.app_context():
        with open('data/customers.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                customer = Customer(name = row['name'], phone = row['phone'], balance = 0)
                db.session.add(customer)
            db.session.commit()

if __name__ == "__main__":
    drop_tables()
    create_tables()
    seed_database()