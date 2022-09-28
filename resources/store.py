import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint("stores", __name__, description="Store Module")


@blp.route('/store/<string:store_id>')
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id], 202
        except KeyError:
            abort(404, message="store not found.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "store deleted."}
        except KeyError:
            abort(404, message="store not found")


@blp.route('/store')
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}, 202

    def post(self):
        data_store = request.get_json()
        if 'name' not in data_store:
            abort(400, message="Bad request. Ensure 'name' is included in JSON payload")
        for store in stores.values():
            if data_store['name'] == store['name']:
                abort(400, message="store already created")
        store_id = uuid.uuid4().hex
        new_store = {"id": store_id, **data_store}
        stores[store_id] = new_store
        return new_store, 201
