#HTTP STATUS CODES

#200 GET successful
#201 CREATED
#202 ACCEPTED --> data has been accepted though it might not update then and there
#404 NOT FOUND
#400 BAD REQUEST

#With Flask RESTful we don't need to use jsonify because it is implicitly used
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
# Resource is just a thing for an api to return, usually mapped in db

app = Flask(__name__)
#Easy to add resources now using Api
app.secret_key = 'sheri'
api = Api(app)

jwt = JWT(app, authenticate, identity) #/auth -> this end point is created by jwt
#from the auth end point, jwt token is returned which takes the username and the password which is then
#passed to the authenticate and identity functions

items = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
        #need to type cast filter, next gives first item called so to avoid any error
        #when no such items are left , None as a default value is used
        item = next(filter(lambda x: x['name'] == name, items), None)
#you need to set http status code because it would give 200
        return {'item' : item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message' : "An item with name {} already exists".format(name)}, 400

        request_data = request.get_json()#force=True)
        #Using force=True, we don;t check Header  ---> content-type
        #silent=True does not give an error
        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message' : 'Item deleted'}

    # def put(self, name):
    #     data = request.get_json()
    #     item = next(filter(lambda x: x['name'] == name, items), None)
    #     if item is None:
    #         item = {'name' : name, 'price' : data['price']}
    #         items.append(item)
    #     else:
    #         item.update(data)
    #     return item

#to make sure that we update arguments only according to our wish out of all other, use reqparse
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price',
            type=float,
            required=True,
            help="This field can't be left blank")
        data = parser.parse_args()
        item = next(filter(lambda x:x['name'] == name, items), None)
        if item is None:
            item = {'name' : name, 'price' : data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items' : items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
app.run(port=5000, debug=True)#5000 is default though
