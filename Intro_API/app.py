from flask import Flask, jsonify, request, render_template
import sys

app = Flask(__name__)
stores = [
    {
        "name": "My Home Store",
        "items": [
            {
                "name": "Charcoal",
                "price": 9.99
            }
        ]
    }
]

@app.route("/")
def home():
    return render_template("index.html")

# POST
@app.route("/store", methods=["POST"])
def create_store():

    request_data = request.get_json()
    new_store = {
        "name": request_data["name"],
        "items": []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET store/some_name_of_store
@app.route("/store/<string:store_name>")
def fetch_store(store_name):
    # return jsonify(store_name)
    print(store_name, file=sys.stderr)
    for store in stores:
        if store["name"].lower() == store_name.lower():
            return jsonify(store)
    return jsonify({"Error": "store not found"})

# GET /store
@app.route("/store")
def get_stores():
    # turn the stores list into a dictionary so jsonify can read it
    return jsonify({"stores": stores})

# POST /store/some_name_of_store/item_price
@app.route("/store/<string:store_name>/item", methods=["POST"])
def add_item_to_store(store_name):
    request_data = request.get_json()
    for store in stores:
        if store["name"].lower() == store_name.lower():
            new_item = {"name": request_data["name"],
                "price": request_data["price"]
                }
            store["items"].append(new_item)
            return jsonify(store["items"])
    return jsonify({"Error": "Something went wrong"})


# GET store/some_store_name/item
@app.route("/store/<string:store_name>/items")
def get_items_in_store(store_name):
    for store in stores:
        if store["name"].lower() == store_name.lower():
            return jsonify({"items": store["items"]})
    return jsonify({"Error": "No items found for that store"})


if __name__ == "__main__":
    # optionally set the port here for use when running as "python app.py"
    # app.run(port=4000)
    app.run()
