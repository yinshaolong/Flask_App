from pathlib import Path
from db import db
from flask import Flask, render_template
import csv
from models import Customer, Product
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
    results = records.scalars()
    return render_template("customers.html", customers=results)
           
@app.route("/products")
def products():
    statement = db.select(Product).order_by(Product.id)
    records = db.session.execute(statement)
    results = records.scalars()
    return render_template("products.html", products=results)


if __name__ == "__main__":
    app.run(debug=True, port=8888)