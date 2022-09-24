from flask import Flask, request
from db import items, stores
import uuid

app = Flask(__name__)


@app.get('/store')
def index():
    return {"stores": list(stores.values())}, 202


@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id], 202
    except KeyError:
        return {"message": "store not found"}


@app.get('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id], 202
    except KeyError:
        return {"message": "item not found"}, 404


@app.get('/item')
def get_items():
    return {"items": list(items.values())}, 202


@app.post('/store')
def create_store():
    data_store = request.get_json()
    if data_store['name'] not in stores.values():
        store_id = uuid.uuid4().hex
        new_store = {"id": store_id, **data_store}
        stores[store_id] = new_store
        return new_store, 201
    return {"message": "store already created"}, 409


@app.post('/item')
def create_item():
    data_item = request.get_json()
    item_id = uuid.uuid4().hex
    new_item = {"id": item_id, **data_item}
    items[item_id] = new_item

    return new_item


if __name__ == '__main__':
    app.run(debug=True, port=5000)
