from flask_restful import Resource, reqparse
from models.store_model import StoreModel


class Store(Resource):

    def get(self, store_name):
        store = StoreModel.find_by_name(store_name)
        if store:
            return store.json()
        return {"message": "Store not found"}, 404

    def post(self, store_name):
        if StoreModel.find_by_name(store_name):
            return {"message": f"{store_name} already exists"}, 400

        store = StoreModel(store_name)

        try:
            store.save_to_db()
        except:
            return {"message": "oops, something went wrong"}, 500

        return store.json(), 201

    def delete(self, store_name):
        store = StoreModel.find_by_name(store_name)
        if store:
            store.delete_from_db()
        return {"message": f"{store_name} has been deleted"}


class StoreList(Resource):
    def get(self):
        return {"Stores": [store.json() for store in StoreModel.query.all()]}
