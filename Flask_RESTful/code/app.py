from flask import Flask, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = [{
    "name": "Charcoal",
    "price": "15.99"
}]


class Item(Resource):
    def get(self, item_name):
        item = filter(lambda x: x["name"].lower() ==
                      item_name.lower(), items)
        # for item in items:
        #     if item["name"].lower() == item_name.lower():
        return item
        # return {"item": "Not found"}, 404

    def post(self, item_name):
        request_data = request.get_json()
        item = {"name": item_name.capitalize(), "price": request_data["price"]}
        items.append(item)
        return item, 201


class Items(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:item_name>")
api.add_resource(Items, "/items")

app.run()
