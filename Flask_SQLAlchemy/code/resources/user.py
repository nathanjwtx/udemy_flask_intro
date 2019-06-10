import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="Username can't be blank")
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="Password can't be blank")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]) is None:
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()
            
            query = "insert into users values (null, ?, ?)"
            cursor.execute(query, (data["username"], data["password"]))

            connection.commit()
            connection.close()

            return {"message": "User created successfully"}, 201
        else:
            return {"message": "User already exists"}, 400