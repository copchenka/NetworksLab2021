import json

from flask import Flask, request, current_app, jsonify

app = Flask(__name__)

storage = {'users': [], 'products': []}


@app.route('/ping')
def hello_world():
    return '.'


@app.route("/users", methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        return json.dumps(storage['users'])
    elif request.method == "POST":
        form = json.loads(request.data)
        if "name" not in form or "balance" not in form:
            return "", 400
        storage["users"].append({"name": form["name"], "balance": form["balance"], "goods": []})
        return form


@app.route("/products", methods=["GET", "POST"])
def reg_product():
    if request.method == "GET":
        return json.dumps(storage['products'])
    elif request.method == "POST":
        form = json.loads(request.data)
        if "name" not in form or "price" not in form:
            return "", 400
        storage["products"].append({"name": form["name"], "price": form["price"]})
        return form


@app.route("/products/<name>", methods=["DELETE", "GET"])
def drop_product(name):
    if request.method == "DELETE":
        storage['products'] = list(filter(lambda el: el["name"] != name, storage["products"]))
        return "."
    else:
        product = list(filter(lambda el: el["name"] == name, storage["products"]))
        if len(product) == 0:
            return "", 400
        else:
            return jsonify(product[0])


@app.route("/users/<username>/<money>/<good>", methods=["POST"])
def add_product(name, money, good):
    product = list(filter(lambda el: el["name"] == good, storage["products"]))
    if len(product) == 0:
        return "no product", 400
    user = list(filter(lambda el: el["name"] == name, storage["users"]))
    if len(user) == 0:
        return "no user", 400
    money -= product[0]["price"]
    if money < 0:
        return "not another money", 400
    i = next((index for (index, d) in enumerate(storage["users"]) if d["name"] == name), None)
    storage["users"][i]["balance"] = money
    return "."


if __name__ == '__main__':
    with app.app_context():
        current_app.token = dict()
    app.run(port=8080)
