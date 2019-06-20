from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, StoreList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
# turn of Flask_SQLAchemy tracker. Leaves the SQLAlcemy tracker in place
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "nathan"
api = Api(app)

# table definitions are imported from the __tablename__ definitions in the
# models
@app.before_first_request
def create_tables():
    db.create_all()


# authenticate and identity are function names from security.py
jwt = JWT(app, authenticate, identity)

api.add_resource(Store, "/store/<string:store_name>")
api.add_resource(Item, "/item/<string:item_name>")
api.add_resource(Items, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(StoreList, "/stores")

from db import db
db.init_app(app)

if __name__ == "__main__":
    # sqlalchemy must be imported here to ensure it is only imported once
    # at run time and not each time app.py is called/imported
    # from db import db
    # db.init_app(app)
    app.run()
