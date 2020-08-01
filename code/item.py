import sqlite3
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field can't be left blank"
        )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name, ))
        item = result.fetchone()
        if item:
            return {"item" : {"name" : item[0], "price" : item[1]}}

    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)
        if item:
            return item
        return {"message" : "Item not found"}, 404

    def post(self, name):
        item = Item.find_by_name(name)
        if item:
            return {'message' : "An item with name {} already exists".format(name)}, 400

        request_data = Item.parser.parse_args()
        item = {'name': name, 'price': request_data['price']}
        try:
            Item.insert(item)
        except Exception:
            {'message': "Couldn't insert in the database"}, 500
        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?,?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        item = Item.find_by_name(name)
        if item is None:
            return {'message' : 'No such item'}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message' : 'Item deleted'}

#to make sure that we update arguments only according to our wish out of all other, use reqparse
    def put(self, name):
        data = Item.parser.parse_args()
        item = Item.find_by_name(name)
        updated_item = {'name' : name, 'price' : data['price']}

        if item is None:
            try:
                Item.insert(updated_item)
            except Exception:
                {'message': "Couldn't insert in the database"}, 500
        else:
            try:
                Item.update(updated_item)
            except Exception:
                {'message': "Couldn't update the database"}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        return {'items' : items}
