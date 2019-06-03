from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "nathan"
api = Api(app)

# authenticate and identity are function names from security.py
jwt = JWT(app, authenticate, identity)

items = [{
    "name": "Charcoal",
    "price": "15.99"
}]


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="Cannot be blank")

    @jwt_required()
    def get(self, item_name):
        item = list(filter(lambda x: x["name"].lower() ==
                    item_name.lower(), items))

        return {"item": item[:1]}, 200 if item else 404

    def post(self, item_name):
        # checking for errors first before working on the payload
        if next(filter(lambda x: x["name"].lower() ==
                       item_name.lower(), items), None):
            return {"Message": f"{item_name} already exists"}, 400

        data = Item.parser.parse_args()

        request_data = request.get_json()
        item = {"name": item_name.capitalize(), "price": request_data["price"]}
        items.append(item)
        return item, 201

    def delete(self, item_name):
        global items
        items = list(filter(lambda x: x["name"].lower() !=
                     item_name.lower(), items))
        return {"message": f"{item_name} deleted"}

    def put(self, item_name):
        # data = request.get_json() # replaced by parser code above
        data = parser.parse_args()
        item = next(filter(lambda x: x["name"].lower() == item_name.lower(),
                    items), None)
        if item is None:
            item = {"name": item_name.capitalize(), "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item


class Items(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:item_name>")
api.add_resource(Items, "/items")

app.run()
