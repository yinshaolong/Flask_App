import csv
from db import db
from app import app
from models import Customer  # import your Customer model

with app.app_context():
    def drop_tables():
            db.drop_all()

    def create_tables():
            db.create_all()

    def seed_database():
            with open('customers.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader)  # skip the header
                for row in reader:
                    customer = Customer(name=row[0]) 
                    db.session.add(customer)
                db.session.commit()

if __name__ == "__main__":
    drop_tables()
    create_tables()
    seed_database()