from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import mapped_column, relationship
from functools import reduce

from db import db
#inherits from db.Model class -> otherwise will not be "registered" by Flask-SQLAlchemy
class Customer(db.Model):
    #primary key / sqlAlch will auto-increment the integer for id
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False, unique=True)
    phone = mapped_column(String(20), nullable=False )
    balance = mapped_column(Numeric(10,2), nullable=False, default=0)
    orders = relationship("Order") #only one back_populates is needed, the other is inferred
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "balance": self.balance,
            "orders": [order.id for order in self.orders]
        }

class Product(db.Model):
    #primary key / sqlAlch will auto-increment the integer for id
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False, unique=True)
    price = mapped_column(Numeric(10,2), nullable=False)
    available = mapped_column(Integer, nullable=False, default=0) #number of products available
    orders = relationship("ProductOrder")

class Order(db.Model):
    id = mapped_column(Integer, nullable=False, primary_key=True)
    customer_id = mapped_column(Integer, ForeignKey(Customer.id), nullable=False)
    customer = relationship("Customer", back_populates="orders")#looks up related enttiy without having to do joins (adds customer_id to the Order table)
    total = mapped_column(Numeric(10,2), nullable=True) #nullable until order is processed by the store
    items = relationship("ProductOrder") 
    def to_json(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "total": self.total,
            "items": [{"product_id": item.product_id, "quantity": item.quantity} for item in self.items]
        }
    def calculate_total(self):
        return round(sum([item.product.price * item.quantity for item in self.items]), 2)
        # self.total = round(reduce(lambda x, y: x + y, [item.product.price * item.quantity for item in self.items]), 2)

class ProductOrder(db.Model):
    id = mapped_column(Integer, nullable=False, primary_key=True)
    order_id = mapped_column(Integer, ForeignKey(Order.id), nullable=False)
    order = relationship("Order", back_populates="items")
    product_id = mapped_column(Integer, ForeignKey(Product.id), nullable=False)
    product = relationship("Product", back_populates="orders")
    quantity = mapped_column(Integer, nullable=False, default=0) #number of orders for this product




