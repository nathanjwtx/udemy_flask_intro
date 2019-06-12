from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
import sqlite3

from models.item_model import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="Cannot be blank")

    @jwt_required()
    def get(self, item_name):
        item = ItemModel.find_by_name(item_name)
        if item:
            return item.json()

        return {"message": "item not found"}, 404

    def post(self, item_name):
        # checking for errors first before working on the payload
        if ItemModel.find_by_name(item_name):
            return {"Message": f"{item_name} already exists"}, 400

        data = Item.parser.parse_args()

        request_data = request.get_json()
        # returning an ItemModel class object not a dictionary now
        item = ItemModel(item_name, data["price"])

        try:
            item.insert()
        except:
            return {"message": "an error occured inserting the item"}, 500

        return item.json(), 201

    def delete(self, item_name):
        connection = sqlite3.connect("code/data.db")
        cursor = connection.cursor()

        query = "delete from items where name=?"
        cursor.execute(query, (item_name.lower().capitalize(),))

        connection.commit()
        connection.close()

        return {"message": f"{item_name} deleted"}

    def put(self, item_name):
        # data = request.get_json() # replaced by parser code above
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(item_name)
        updated_item = ItemModel(name, data["price"])

        if item is None:
            try:
                updated_item.insert()
            except:
                return {"Message": "An error occured inserting the item"}, 500
        else:
            try:
                updated_item.update()
            except:
                return {"Message": "An error occured updating the item"}, 500

        return updated_item.json()


class Items(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "select * from items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({"Name": row[1], "Price": row[2]})

        connection.close()
        return {"items": items}
