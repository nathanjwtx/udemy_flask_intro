from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required

from models.item_model import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="Cannot be blank")

    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="Items need a store id")

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
        item = ItemModel(item_name, data["price"], data["store_id"])

        try:
            item.save_to_db()
        except:
            return {"message": "an error occured inserting the item"}, 500

        return item.json(), 201

    def delete(self, item_name):
        item = ItemModel.find_by_name(item_name)
        if item:
            item.delete_from_db()
        return {"message": "Item deleted"}

    def put(self, item_name):
        # data = request.get_json() # replaced by parser code above
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(item_name)

        if item is None:
            item = ItemModel(item_name, data["price"], data["store_id"])
        else:
            item.price = data["price"]
        
        item.save_to_db()
        return item.json()


class Items(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
        # using lambda
        # return {"items": list(map[lambda x: x.json(), ItemModel.query.all()])}
