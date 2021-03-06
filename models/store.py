import sqlite3
from db import db

class StoreModel(db.Model):

    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship('ItemModel')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
        "id" : self.id,
        "name" : self.name,
        "items" : [item.json() for item in self.items]}

    @classmethod
    def find_by_name(cls, name):
        #.query() comes from sqlalchemy and it returns row object
        #connections and all are handled implicitly
        #.query, .filter are query builders
        #eg:- filter_by(name=name).first() is same as -->
        #SELECT * FROM items WHERE name=name LIMIT 1 which converts to ItemModel object
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        #we don't need insert & update functions separately now because
        #following commands handle both
        db.session.add(self) #now this is capable of inserting & updating rows
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
