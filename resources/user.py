import sqlite3
from flask_restful import Resource, request, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field can't be blank"
        )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field can't be blank"
        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message" : "A user with username - {} already exists".format(data['username'])}

        user = UserModel(**data)#unpacking a dictionary, for unpacking a tuple *(single star is used)
        user.save_to_db()

        return {"message" : "User created successfully"}, 201
