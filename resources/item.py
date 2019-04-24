from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="can not be blank"
    )

    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="can not be blank"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "not found"}, 404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {"message": "{} item has already exist".format(name)}, 404

        data = Item.parser.parse_args()
        newitem = ItemModel(**data)
        try:
            newitem.save_to_db()
        except:
            return {"message": "An error occurred"}

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_databae()
        return {'message': "item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name()
        if item:
            item.price = data['price']
        else:
            item = ItemModel(**data)

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": x.json for x in ItemModel.query.all()}