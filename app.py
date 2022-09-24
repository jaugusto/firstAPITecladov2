from flask import Flask, request
from db import items, stores
import uuid
from flask_smorest import abort

app = Flask(__name__)


@app.get('/item')
def get_items():
    return {"items": list(items.values())}, 202


@app.get('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id], 202
    except KeyError:
        abort(404, message="item not found.")


@app.post('/item')
def create_item():
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


@app.put('/item/<string:item_id>')
def update_item(item_id):
    item_data = request.get_json()
    if "name" not in item_data or "price" not in item_data:
        abort(404, message="Bad request. Ensure 'name' or 'price' in JSON payload")
    try:
        item = items[item_id]
        item = {**item, **item_data}
        return item
    except KeyError:
        abort(404, message="item not found")


@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "item deleted"}
    except KeyError:
        abort(404, message="item not found")


@app.get('/store')
def index():
    return {"stores": list(stores.values())}, 202


@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id], 202
    except KeyError:
        abort(404, message="store not found.")


@app.post('/store')
def create_store():
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


@app.delete('/store/<string:store_id>')
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "store deleted."}
    except KeyError:
        abort(404, message="store not found")


if __name__ == '__main__':
    app.run(debug=True, port=5000)
