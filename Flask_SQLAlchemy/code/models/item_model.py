import sqlite3
from db import db


class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def json(self):
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, item_name):
        connection = sqlite3.connect("code/data.db")
        cursor = connection.cursor()

        query = "select * from items where name = ?"
        result = cursor.execute(query, (item_name.lower().capitalize(),))
        row = result.fetchone()
        connection.close()

        if row:
            # return cls(row[0], row[1])
            # arguement unpacking
            return cls(*row)

    def insert(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "insert into items values (null, ?, ?)"
        cursor.execute(query, (self.name.lower().capitalize(), self.price,))

        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = ("update items set price = ? where name = ?")
        cursor.execute(query, (self.price, self.name,))

        connection.commit()
        connection.close()
