import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores

blp = Blueprint('items', __name__, description="Item module")


@blp.route('/item/<string:item_id>')
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id], 202
        except KeyError:
            abort(404, message="item not found.")

    def put(self, item_id):
        item_data = request.get_json()
        if "name" not in item_data or "price" not in item_data:
            abort(404, message="Bad request. Ensure 'name' or 'price' in JSON payload")
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
    def get(self):
        return {"items": list(items.values())}, 202

    def post(self):
        data_item = request.get_json()
        if "price" not in data_item or "store_id" not in data_item or "name" not in data_item:
            abort(400, message="Bad request. Ensure 'price', 'store_id' and 'name' are included in JSON.")
        for item in items.values():
            if data_item['store_id'] == item['store_id'] and data_item['name'] == item['name']:
                abort(400, message="item already created")
        if data_item["store_id"] not in stores:
            abort(404, message="store not found.")
        item_id = uuid.uuid4().hex
        new_item = {"id": item_id, **data_item}
        items[item_id] = new_item
        return new_item
