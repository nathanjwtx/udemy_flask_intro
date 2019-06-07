from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="Cannot be blank")

    @jwt_required()
    def get(self, item_name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "select * from items where name like ?"
        result = cursor.execute(query, (item_name.lower(),))
        row = result.fetchone()
        connection.close()

        if row:
            return {"Item": {"name": row[0], "price": row[1]}}
        return {"message": "item not found"}

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