from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def json(self):
        # need to use json as self.items is an object or list
        return {"name": self.name,
                "items": [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, store_name):
        return cls.query.filter_by(name=store_name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
