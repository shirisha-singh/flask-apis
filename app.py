#HTTP STATUS CODES

#200 GET successful
#201 CREATED
#202 ACCEPTED --> data has been accepted though it might not update then and there
#404 NOT FOUND
#400 BAD REQUEST
#500 INTERNAL SERVER ERROR

#With Flask RESTful we don't need to use jsonify because it is implicitly used
from flask import Flask
from db import db
from flask_restful import Api
from flask_jwt import JWT
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from security import authenticate, identity
# Resource is just a thing for an api to return, usually mapped in db

app = Flask(__name__)
db.init_app(app)
#Easy to add resources now using Api
#Flask-SQLAlchemy tracks every change made to db even if not saved,
#which takes up some resources, so we turn this off, SQLAlchemy already
#has a better modification tracker
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'sheri'
api = Api(app)

#before the first request runs(any request), this code runs to create data.db file
@app.before_first_request#flask decorator
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) #/auth -> this end point is created by jwt
#from the auth end point, jwt token is returned which takes the username and the password which is then
#passed to the authenticate and identity functions


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    app.run(port=5000, debug=True)#5000 is default though
