from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from db import db
#inherits from db.Model class -> otherwise will not be "registered" by Flask-SQLAlchemy
class Customer(db.Model):
    #primary key / sqlalch will auto-increment the integer for id
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False, unique=True)
    phone = mapped_column(String(20), nullable=False )
    balance = mapped_column(Numeric, nullable=False, default=0)

class Product(db.Model):
    #primary key / sqlalch will auto-increment the integer for id
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False, unique=True)
    price = mapped_column(Numeric, nullable=False)
    available = mapped_column(Integer, nullable=False, default=0)

class Order(db.Model):
    id = mapped_column(Integer, nullable=False, primary_key=True)
    customer_id = mapped_column(Integer, ForeignKey("customer.id"), nullable=False)
    total = mapped_column(Numeric, nullable=False)

class ProductOrder(db.Model):
    id = mapped_column(Integer, nullable=False, primary_key=True)
    order_id = mapped_column(Integer, ForeignKey("order.id"), nullable=False)
    product_id = mapped_column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = mapped_column(Integer, nullable=False)




