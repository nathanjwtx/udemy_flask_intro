from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items

app = Flask(__name__)
app.secret_key = "nathan"
api = Api(app)

# authenticate and identity are function names from security.py
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, "/item/<string:item_name>")
api.add_resource(Items, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    app.run()
