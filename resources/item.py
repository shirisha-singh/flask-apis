import sqlite3
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity, fresh_jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field can't be left blank"
        )
    parser.add_argument('store_id',
       type=int,
       required=True,
       help="Every item needs a store id"
       )

    @jwt_required #without brackets for flask_jwt_exteded
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message" : "Item not found"}, 404

    @fresh_jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message' : "An item with name {} already exists".format(name)}, 400

        request_data = Item.parser.parse_args()

        item = ItemModel(name, **request_data)

        try:
            item.save_to_db()
        except Exception:
            return {'message': "Couldn't insert in the database"}, 500
        return item.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message' : 'Admin privilege required'}, 401
        item = ItemModel.find_by_name(name)
        if item is None:
            return {'message' : 'No such item'}
        item.delete_from_db()
        return {'message' : 'Item has been deleted'}

#to make sure that we update arguments only according to our wish out of all other, use reqparse
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item = ItemModel(name, **data)
            except Exception:
                {'message': "Couldn't insert in the database"}, 500
        else:
            try:
                item.price = data['price']
            except Exception:
                return {'message': "Couldn't update the database"}, 500
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.query.all()]
        if user_id:
            return {'items' : items}, 200
        return{
            'items' : [item.name for item in ItemModel.query.all()],
            'message' : 'More data available on log in'
        }, 200
