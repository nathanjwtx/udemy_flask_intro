from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="Cannot be blank")

    @classmethod
    def find_by_name(cls, item_name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "select * from items where name = ?"
        result = cursor.execute(query, (item_name.lower().capitalize(),))
        row = result.fetchone()
        connection.close()

        if row:
            return {"Item": {"name": row[0], "price": row[1]}}

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "insert into items values (null, ?, ?)"
        cursor.execute(query, (item["name"], item["price"],))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = ("update items set price = ? where name = ?")
        cursor.execute(query, (item["price"], item["name"],))

        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, item_name):
        item = self.find_by_name(item_name)
        if item:
            return item

        return {"message": "item not found"}, 404

    def post(self, item_name):
        # checking for errors first before working on the payload
        if self.find_by_name(item_name):
            return {"Message": f"{item_name} already exists"}, 400

        data = Item.parser.parse_args()

        request_data = request.get_json()
        item = {"name": item_name.capitalize(), "price": request_data["price"]}

        try:
            self.insert(item)
        except:
            return {"message": "an error occured inserting the item"}, 500

        return item, 201

    def delete(self, item_name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "delete from items where name=?"
        cursor.execute(query, (item_name.lower().capitalize(),))

        connection.commit()
        connection.close()

        return {"message": f"{item_name} deleted"}

    def put(self, item_name):
        # data = request.get_json() # replaced by parser code above
        data = Item.parser.parse_args()
        item = self.find_by_name(item_name)
        updated_item = {"name": item_name.lower().capitalize(), "price": data["price"]}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"Message": "An error occured inserting the item"}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"Message": "An error occured updating the item"}, 500

        return updated_item


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
