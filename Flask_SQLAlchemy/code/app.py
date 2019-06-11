from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items

app = Flask(__name__)
# turn of Flask_SQLAchemy tracker. Leaves the SQLAlcemy tracker in place
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "nathan"
api = Api(app)

# authenticate and identity are function names from security.py
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, "/item/<string:item_name>")
api.add_resource(Items, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    # sqlalchemy must be imported here to ensure it is only imported once
    # at run time and not each time app.py is called/imported
    from db import db
    db.init_app(app)
    app.run()
