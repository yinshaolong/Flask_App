import requests
import webbrowser

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
    post("/api/products", {"name": "salty nuts", "price": 6.99})
    input("Next: Check for salty nuts in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + "/products")
    input("Press Enter to continue.")


ok_order = {
    "customer_id": 1,
    "items": [
        {"name": "apple", "quantity": 1},
        {"name": "bananas", "quantity": 1},
        {"name": "lemon", "quantity": 1},
    ],
}

nok_order_1 = {
    "customer_id": 2,
    "items": [
        {"name": "onions", "quantity": 200},
        {"name": "raspberries", "quantity": 140},
        {"name": "chicken breast", "quantity": 30},
    ],
}
nok_order_2 = {
    "customer_id": 3,
    "items": [
        {"name": "eggs", "quantity": 2},
        {"name": "cheese", "quantity": 1},
        {"name": "milk", "quantity": 190},
    ],
}

orders = get("/api/orders").json()
next_id = max(order["id"] for order in orders) + 1


def demo_5():
    print("\n=====Demo 5=====")

    # 1. Add new products
    input("Next: Add new products. Press Enter when ready.")

    print("Adding a new product: 'unsalted nuts' (7.00)")
    post("/api/products", {"name": "unsalted nuts", "price": 7.00})
    print("Adding a second new product: 'celery' (2.49)")
    post("/api/products", {"name": "celery", "price": 2.49})
    print("Adding a third new product: 'guava' (4.00)")
    post("/api/products", {"name": "guava", "price": 4.00})

    # 2. Make new orders
    input("Next: Make new orders. Press Enter when ready.")

    print(f"Adding an OK order (id {next_id})")
    post("/api/orders", ok_order)
    print(f"Adding a NOK order (id {next_id + 1})")
    post("/api/orders", nok_order_1)
    print(f"Adding a second NOK order (id {next_id + 2})")
    post("/api/orders", nok_order_2)

    # 3. Open HTML interface
    input(
        "Next: Check for new products and orders in the web pages. Press Enter when ready."
    )
    webbrowser.open(FLASK_URL + "/products")
    input("Press Enter to continue.")


def demo_6():
    order_id = next_id
    print("\n=====Demo 6=====")

    # 1. Open HTML interface
    input(
        "Next: Check customer balance and product stock in the web pages. Press Enter when ready."
    )
    webbrowser.open(FLASK_URL + "/customers")

    # 2. Process OK order
    input("Next: Process the OK order. Press Enter when ready.")
    print("Processing with default strategy...")
    put(f"/api/orders/{order_id}", {"process": True})

    # 0. Check customer balance and product stock with API
    input("Next: Check customer 1 balance. Press Enter when ready.")
    print(get(f"/api/customers/1").json())
    input("Next: Check product stock (1, 2, 3). Press Enter when ready.")
    print(get(f"/api/products/1").json())
    print(get(f"/api/products/2").json())
    print(get(f"/api/products/3").json())
    input("Press Enter to continue.")


def demo_7():
    order_id = next_id + 1
    print("\n=====Demo 7=====")

    # 0. Check customer balance and product stock with API
    input("Next: Check customer 2 balance. Press Enter when ready.")
    print(get(f"/api/customers/2").json())
    input("Next: Check product stock (7, 5, 10). Press Enter when ready.")
    print(get(f"/api/products/7").json())
    print(get(f"/api/products/5").json())
    print(get(f"/api/products/10").json())

    # 1. Process first NOK order with reject strategy
    input("Next: Process the NOK order with reject strategy. Press Enter when ready.")
    print("Processing with reject strategy...")
    put(f"/api/orders/{order_id}", {"process": True, "strategy": "reject"})

    # 2. Open HTML interface
    input("Next: Check order detail in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + f"/orders/{order_id}")

    # 3. with ignore strategy
    input("Next: Process the OK order with ignore strategy. Press Enter when ready.")
    print("Processing with ignore strategy...")
    put(f"/api/orders/{order_id}", {"process": True, "strategy": "ignore"})

    # 4. Open HTML interface
    input("Next: Check order detail in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + f"/orders/{order_id}")
    input("Press Enter to continue.")


def demo_8():
    order_id = next_id + 2
    print("\n=====Demo 8=====")

    # 0. Check customer balance and product stock with API
    input("Next: Check customer 3 balance. Press Enter when ready.")
    print(get(f"/api/customers/3").json())
    input("Next: Check product stock (15, 13, 14). Press Enter when ready.")
    print(get(f"/api/products/15").json())
    print(get(f"/api/products/13").json())
    print(get(f"/api/products/14").json())

    # 1. Process second NOK order with default strategy
    input("Next: Process the NOK order with default strategy. Press Enter when ready.")
    print("Processing with default strategy...")
    put(f"/api/orders/{order_id}", {"process": True})

    # 2. Open HTML interface
    input("Next: Check order detail in the web page. Press Enter when ready.")
    webbrowser.open(FLASK_URL + f"/orders/{order_id}")
    input("Press Enter to continue.")


def demo_9():
    print("\n=====Demo 9=====")
    input("Use Postman. Press Enter when done.")


if __name__ == "__main__":
    # demo()
    demo_5()
    demo_6()
    demo_7()
    demo_8()
    demo_9()
