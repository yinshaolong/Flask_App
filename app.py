from pathlib import Path
from db import db
from flask import Flask
# from routes.api_customers import api_customers_bp
# from routes.api_orders import api_orders_bp
# from routes.api_products import api_products_bp
from routes import api_customers_bp, api_orders_bp, api_products_bp, html_bp

app = Flask(__name__)
#this will make flask use a 'sqlite database witht the filename provided
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///store.db"
#this will make flask store the database file inthe path provided
#use "." for the instance path
app.instance_path = Path(".").resolve()
#connects db object with the app object - line 5
db.init_app(app)

app.register_blueprint(api_customers_bp, url_prefix="/api/customers")
app.register_blueprint(api_orders_bp, url_prefix="/api/orders")
app.register_blueprint(api_products_bp, url_prefix="/api/products")
app.register_blueprint(html_bp, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True, port=8888)