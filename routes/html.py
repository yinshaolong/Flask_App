from db import db
from flask import  Blueprint, redirect, url_for, render_template
from models import Customer, Product, Order, ProductOrder


html_bp = Blueprint("html", __name__)

@html_bp.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@html_bp.route("/customers", methods=["GET"])
def customers():
    statement = db.select(Customer).order_by(Customer.id)
    records = db.session.execute(statement)
    results = records.scalars() #converts into a list
    return render_template("customers.html", customers=results)
           
@html_bp.route("/products", methods=["GET"])
def products():
    statement = db.select(Product).order_by(Product.id)
    records = db.session.execute(statement)
    results = records.scalars()
    return render_template("products.html", products=results)


@html_bp.route("/customers/<int:customer_id>", methods=["GET"])
def customer_detail(customer_id):
    # print("in customer details")
    # statement = db.select(Customer).where(Customer.id == customer_id)
    # result = db.session.execute(statement)
    # customer = result.scalar()
    customer = db.get_or_404(Customer, customer_id) #does the same thing as line above, but also returns the 404 error if not found
    return render_template("customer_detail.html", customer=customer)


@html_bp.route("/orders/<int:order_id>", methods=["GET"])
def order_detail(order_id):
    order = db.get_or_404(Order, order_id) #does the same thing as line above, but also returns the 404 error if not found
    return render_template("order_detail.html", order=order)


@html_bp.route("/orders", methods=["GET"])
def orders():
    statement = db.select(Order).order_by(Order.id)
    records = db.session.execute(statement)
    results = records.scalars()
    return render_template("orders.html", orders=results)

    
@html_bp.route("/orders/<int:order_id>/delete", methods=["POST"])
def order_delete(order_id):
    order = db.get_or_404(Order, order_id)
    if not order.processed: #disable functionality to prevent bad people from trigging request without form
        db.session.delete(order)
        db.session.commit()
        return redirect(url_for("html.orders"))
    return redirect(url_for("html.order_detail", order_id=order_id)) #refresh page

@html_bp.route("/orders/<int:order_id>", methods=["POST"])
def order_process(order_id):
    order = db.get_or_404(Order, order_id)
    strategy = "adjust"
    # strategy = "reject" 
    # strategy = "ignore" 
    if not order.processed:
        process = order.process_order(strategy)
        print("order processed", process, order.processed)
        db.session.commit()
        return redirect(url_for("html.orders"))
    return redirect(url_for("html.order_detail", order_id=order_id)) #refresh page
