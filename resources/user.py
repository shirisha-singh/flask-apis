import sqlite3
from flask_restful import Resource, request, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,get_raw_jwt, jwt_required, create_refresh_token, jwt_refresh_token_required, get_jwt_identity

from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
       'username',
        type=str,
        required=True,
        help="This field can't be blank"
        )
_user_parser.add_argument(
       'password',
        type=str,
        required=True,
        help="This field can't be blank"
        )

class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message" : "A user with username - {} already exists".format(data['username'])}

        user = UserModel(**data)#unpacking a dictionary, for unpacking a tuple *(single star is used)
        user.save_to_db()

        return {"message" : "User created successfully"}, 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message' : 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message' : 'User not found'}, 404
        user.delete_from_db()
        return {'message' : 'User deleted successfully'}, 200

class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        print(user)
        if user and safe_str_cmp(data['password'], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=


            user.id)
            return{
              'access_token' : access_token,
              'refresh_token' : refresh_token
            }, 200
        return {'message' : 'Invalid credentials'}, 401

class UserLogout(Resource):
#just  the current access token and not users
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']#jti is 'JTI ID', a unique identifier for jwt
        BLACKLIST.add(jti)
        return {
            'message' : 'Successfully logged out'
        }

class TokenRefresher(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token' : new_token}, 200
