from flask_restful import Resource, reqparse, request
from models.user import UserModel
import sqlite3


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field can not be blank"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field can not be blank"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_name(data['username']):
            return {'message': 'the user exists'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created ok"}, 201
