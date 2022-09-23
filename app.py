from flask import Flask, request, jsonify


app = Flask(__name__)

stores = [
    {
        "name": "Armazem Paraiba",
        "items": [
            {
                "name": "cadeira",
                "price": 340
            },
            {
                "name": "mesa",
                "price": 700
            }
        ]
    }
]


@app.get('/store')
def index():
    return jsonify(stores)


@app.get('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({"message": "Store not found"})


@app.get('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store['items'])
    return jsonify({"message": "Store not found"})


@app.post('/store')
def create_store():
    data = request.get_json()
    if data['name'] not in [store['name'] for store in stores]:
        stores.append({"name": data['name'], "items": []})
        return jsonify(stores)
    return {"message": "Store already created!"}


@app.post('/store/<string:name>/item')
def create_item_in_store(name):
    data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': data['name'],
                'price': data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return {"message": "Store not found"}


if __name__ == '__main__':
    app.run(debug=True, port=5000)
