from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="can not be blank"
    )

    @jwt_required
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "not found"}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message": "{} store has already exist".format(name)}, 404

        data = Store.parser.parse_args()
        newitem = StoreModel(**data)
        try:
            newitem.save_to_db()
        except:
            return {"message": "An error occurred"}

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_databae()
        return {'message': "store deleted"}

    def put(self, name):
        data = Store.parser.parse_args()
        store = StoreModel.find_by_name()
        if store:
            store.price = data['price']
        else:
            store = StoreModel(**data)

        store.save_to_db()
        return store.json()


class StoreList(Resource):
    def get(self):
        return {"items": x.json for x in StoreModel.query.all()}