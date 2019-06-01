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
        item = list(filter(lambda x: x["name"].lower() ==
                    item_name.lower(), items))
        # next(list(), None)

        return {"item": item[:1]}, 200 if item else 404

    def post(self, item_name):
        if next(filter(lambda x: x["name"].lower() ==
                        item_name.lower(), items), None):
            return {"Message": f"{item_name} already exists"}, 400
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
