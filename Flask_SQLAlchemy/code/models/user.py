import sqlite3
from db import db


class UserModel(db.Model):
    # SQLAlchemy model setup
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, user_id, username, password):
        # MUST be self.id else it will not work with flask_JWT idenity function
        # property names must match model names in order to be saved in db
        # not all properties have to be saved to db
        self.id = user_id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect("code/data.db")
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
        connection = sqlite3.connect("/code/data.db")
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