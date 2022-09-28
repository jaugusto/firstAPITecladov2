import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint('items', __name__, description="Item module")


@blp.route('/item/<string:item_id>')
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id], 202
        except KeyError:
            abort(404, message="item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="item not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "item deleted"}
        except KeyError:
            abort(404, message="item not found")


@blp.route('/item')
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, data_item):
        for item in items.values():
            if data_item['store_id'] == item['store_id'] and data_item['name'] == item['name']:
                abort(400, message="item already created")
        if data_item["store_id"] not in stores:
            abort(404, message="store not found.")
        item_id = uuid.uuid4().hex
        new_item = {"id": item_id, **data_item}
        items[item_id] = new_item
        return new_item
