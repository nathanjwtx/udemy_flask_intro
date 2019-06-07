import sqlite3
from flask_restful import Resource, reqparse

class User(object):
    def __init__(self, user_id, username, password):
        # MUST be self.id else it will not work with flask_JWT idenity function
        self.id = user_id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "select * from users where username=?"
        # arguments to execute must a tuple, eg (username,)
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2])  # or cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "select * from users where id=?"
        # arguments to execute must a tuple, eg (username,)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2])  # or cls(*row)
        else:
            user = None

        connection.close()
        return user


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

        if User.find_by_username(data["username"]) is None:
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()
            
            query = "insert into users values (null, ?, ?)"
            cursor.execute(query, (data["username"], data["password"]))

            connection.commit()
            connection.close()

            return {"message": "User created successfully"}, 201
        else:
            return {"message": "User already exists"}, 400