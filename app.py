#HTTP STATUS CODES

#200 GET successful
#201 CREATED
#202 ACCEPTED --> data has been accepted though it might not update then and there
#404 NOT FOUND
#400 BAD REQUEST
#500 INTERNAL SERVER ERROR

#With Flask RESTful we don't need to use jsonify because it is implicitly used
import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager


from resources.user import UserRegister, User, UserLogin, TokenRefresher, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST
# Resource is just a thing for an api to return, usually mapped in db

app = Flask(__name__)
#Easy to add resources now using Api
#Flask-SQLAlchemy tracks every change made to db even if not saved,
#which takes up some resources, so we turn this off, SQLAlchemy already
#has a better modification tracker
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
#DATABASE_URL is the name of the environment variable that heroku sets for us,
#but this can't be accessed on local as postgresql is not installed on local & hence
#letting sqlite uri gives us a fall-back option, now this would work on local as well
#but would use sqlite, on heroku app would use postgresql
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPOGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh'] #enable it for both accessed & refreshed tokens
app.secret_key = 'sheri' #used to encrypt JWT key, can also go for app.config['JWT_SECURITY_KEY']
api = Api(app)

#before the first request runs(any request), this code runs to create data.db file
@app.before_first_request#flask decorator
def create_tables():
    db.create_all()

jwt = JWTManager(app) #does not create /auth

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: #should be read from a config file or database
        return {'is_admin' : True}
    return {'is_admin' : False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description' : 'The token has expired',
        'error' : 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description' : 'Signature verification failed',
        'error' : 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description' : 'Request does not contain an access token',
        'error' : 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description' : 'The token is not fresh',
        'error' : 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description' : 'The token has been revoked',
        'error' : 'token_revoked'
    }), 401

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresher, '/refresh')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)#5000 is default though
