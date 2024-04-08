import requests
import webbrowser

# CHANGE THE VARIABLE BELOW TO YOUR FLASK URL
FLASK_URL = "http://localhost:8888"


def http(method, path, data=None):
    print(f"Making {method} request to {FLASK_URL + path}...")
    if method not in ["GET", "POST", "PUT", "DELETE"]:
        raise RuntimeWarning("Invalid method")
    
    if method == "GET":
        response = requests.get(FLASK_URL + path)
    elif method == "POST":
        response = requests.post(FLASK_URL + path, json=data)
    elif method == "PUT":
        response = requests.put(FLASK_URL + path, json=data)
    elif method == "DELETE":
        response = requests.delete(FLASK_URL + path)
    
    print("Received status code:", response.status_code)
    return response

def get(path):
    return http("GET", path)


def post(path, data=None):
    return http("POST", path, data)


def put(path, data=None):
    return http("PUT", path, data)


def delete(path):
    return http("DELETE", path)


def demo():
    print("Adding a new product: 'salty nuts' (6.99)")
    post("/api/products/", {"name": "salty nuts", "price": 6.99})
    input("Check for salty nuts in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/products")
    input("Press Enter to continue.")
#python manage.py

def demo1():
    print("Adding a new product: 'baguette' (2.99)")
    post("/api/products/", {"name": "baguette", "price": 2.99})
    print("Adding a new product: 'croissant' (1.99)")
    post("/api/products/", {"name": "croissant", "price": 1.99})
    print("Adding a new product: 'pain au chocolat' (1.99)")
    post("/api/products/", {"name": "pain au chocolat", "price": 1.99})
    print("Adding a new product: 'pain aux raisins' (1.99)")
    post("/api/products/", {"name": "pain aux raisins", "price": 1.99})

    input("Check for baguette, croissant, pain au chocolat, and pain aux raisins in the web page. Press Enter when ready.")

    NOK_order_1 = {
        "customer_id": 1,
        "items": [
            {"name": "ground beef", "quantity": 99999999},
            {"name": "bananas", "quantity": 99999999},
            {"name": "chicken thigh", "quantity": 99999999}
        ]
    }
    NOK_order_2 = {
        "customer_id": 2,
        "items": [
            {"name": "orange", "quantity": 99999999},
            {"name": "potato", "quantity": 99999999},
            {"name": "cheese", "quantity": 99999999}
        ]
    }
    OK_order_3 = {
        "customer_id": 3,
        "items": [
            {"name": "milk", "quantity": 1},
            {"name": "eggs", "quantity": 1},
            {"name": "bread", "quantity": 1}
        ]
    }
    post('/api/orders',NOK_order_1)
    post('/api/orders', NOK_order_2)
    post('/api/orders', OK_order_3)
    webbrowser.open(FLASK_URL + "/products")
    input("Press Enter to continue.")

def demo2():
    put("/api/orders/13", {"processed": True})
    print(get(f"/api/customers/3").json())
    input("Press Enter to continue.")
    print(get(f"/api/products/14").json())
    input("Press Enter to continue.")
    print(get(f"/api/products/15").json())
    input("Press Enter to continue.")
    print(get(f"/api/products/9").json())
    input("Press Enter to continue.")

def demo3():
    put("/api/orders/11", {"processed": True, "strategy": "reject"})
    print(get(f"/api/customers/1").json())
    input("Press Enter to continue.")
    print(get(f"/api/products/12").json())
    
    input("Press Enter to continue.")
    print(get(f"/api/products/2").json())
    
    input("Press Enter to continue.")
    print(get(f"/api/products/11").json())
    #ignore
    put("/api/orders/11", {"processed": True, "strategy": "ignore"})
    print(get(f"/api/customers/1").json())
    input("Press Enter to continue.")
    print(get(f"/api/products/12").json())
    
    input("Press Enter to continue.")
    print(get(f"/api/products/2").json())
    
    input("Press Enter to continue.")
    print(get(f"/api/products/11").json())
    
def demo4():
    put("/api/orders/12", {"processed": True, "strategy": "adjust"})
    print(get(f"/api/customers/2").json())
    input("Press Enter to continue.")
    print(get(f"/api/products/4").json())
    
    input("Press Enter to continue.")
    print(get(f"/api/products/6").json())
    
    input("Press Enter to continue.")
    print(get(f"/api/products/13").json())


if __name__ == "__main__":
    # demo()
    demo1()
    demo2()
    demo3()
    demo4()

