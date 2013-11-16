#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, \
    url_for, render_template, Response
import datetime
import pymongo
from pymongo import Connection
from bson import json_util
import json
from bson.json_util import loads

app = Flask(__name__, static_folder='../app', static_url_path='',
            template_folder='../app')

server = "ds053948.mongolab.com"
port = 53948
db_name = 'words'
username = "admin"
password = "iicenajv"

con = Connection(server, port)
db = con[db_name]
db.authenticate(username, password)
words = db.words
users = db.users


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")


@app.route('/api/words/', methods=['GET'])
def get_words():
    l_words = list(words.find())
    Jsonwords = json.dumps(l_words, sort_keys=True, default=json_util.default)
    decoded = json.loads(Jsonwords)
    return jsonify({"words": decoded})


@app.route('/api/words/<int:word_id>/', methods=['GET'])
def get_id_word(word_id):
    Jsonwords = json.dumps(words.find_one({"id": word_id}), sort_keys=True,
                           default=json_util.default)
    Jsonpage = Response(response=Jsonwords, mimetype="application/json")
    return Jsonpage

@app.route('/api/words/<word>/', methods=['GET'])
def get_word(word):
    Jsonwords = json.dumps(words.find_one({"word": word}), sort_keys=True,
                           default=json_util.default)
    Jsonpage = Response(response=Jsonwords, mimetype="application/json")
    return Jsonpage


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/words/', methods=['POST'])
def create_word():
    if not request.json or not 'word' in request.json:
        abort(400)
    l_words = list(words.find())
    item = {
        'id': l_words[-1]['id'] + 1,
        'word': request.json["word"],
        'translation': request.json.get('translation', ""),
        'knowIndex': 2
    }
    words.insert(item)
    Jsonwords = json.dumps(item, sort_keys=True, default=json_util.default)
    decoded = json.loads(Jsonwords)
    return jsonify({"item": decoded}), 201


@app.route('/api/words/<int:word_id>/', methods=['PUT'])
def update_word(word_id):
    item = words.find_one({"id": word_id})
    if len(item) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'word' in request.json and type(request.json['word']) != unicode:
        abort(400)
    if 'translation' in request.json and \
            type(request.json['translation']) is not unicode:
        abort(400)
    if 'knowIndex' in request.json and type(request.json['done']) is not int:
        abort(400)
    item['word'] = request.json.get('word', item['word'])
    item['translation'] = request.json.get('translation', item['translation'])
    item['knowIndex'] = request.json.get('knowIndex', item['knowIndex'])
    n_item = {}
    for data in item:
        if data != "_id":
            n_item[data] = item[data]
    words.update({'_id': item['_id']}, {"$set": n_item}, upsert=False)
    return jsonify({'user': n_item})

    return jsonify({'item': n_item})

    user = users.find_one({"username": user_name})
    if len(user) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'username' in request.json and \
            type(request.json['username']) != unicode:
        abort(400)
    if 'password' in request.json and \
            type(request.json['password']) != unicode:
        abort(400)
    if 'email' in request.json and type(request.json['email']) != unicode:
        abort(400)

    user['username'] = request.json.get('username', user['username'])
    user['password'] = request.json.get('password', user['password'])
    user['email'] = request.json.get('email', user['email'])
    user['words'] = request.json.get('words', user['words'])


@app.route('/api/words/<int:word_id>/', methods=['DELETE'])
def delete_word(word_id):
    item = words.find_one({"id": word_id})
    if len(item) == 0:
        abort(404)
    words.remove(item)
    return jsonify({'result': True})


@app.route('/api/users/', methods=['GET'])
def get_users():
    l_users = list(users.find())
    Jsonwords = json.dumps(l_users, sort_keys=True, default=json_util.default)
    decoded = json.loads(Jsonwords)
    return jsonify({"words": decoded})


@app.route('/api/users/<user_name>/', methods=['GET'])
def get_user(user_name):
    if str(json.dumps(users.find_one({"name": user_name}),
           sort_keys=True, default=json_util.default)) != "null":
        Jsonwords = json.dumps(users.find_one({"name": user_name}),
                               sort_keys=True, default=json_util.default)
    else:
        Jsonwords = json.dumps(users.find_one({"username": user_name}),
                               sort_keys=True, default=json_util.default)
    Jsonpage = Response(response=Jsonwords, mimetype="application/json")
    return Jsonpage


@app.route('/api/users/', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    l_users = list(users.find())
    user = {
        'username': request.json["username"],
        'password': request.json["password"],
        'email': request.json["email"],
        'words': []
    }
    users.insert(user)
    Jsonwords = json.dumps(user, sort_keys=True, default=json_util.default)
    decoded = json.loads(Jsonwords)
    return jsonify({'user': decoded}), 201


@app.route('/api/users/<user_name>/', methods=['PUT'])
def update_user(user_name):
    user = users.find_one({"username": user_name})
    if len(user) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'username' in request.json and \
            type(request.json['username']) != unicode:
        abort(400)
    if 'password' in request.json and \
            type(request.json['password']) != unicode:
        abort(400)
    if 'email' in request.json and type(request.json['email']) != unicode:
        abort(400)

    user['username'] = request.json.get('username', user['username'])
    user['password'] = request.json.get('password', user['password'])
    user['email'] = request.json.get('email', user['email'])
    user['words'] = request.json.get('words', user['words'])
    n_user = {}
    for data in user:
        if data != "_id":
            n_user[data] = user[data]
    users.update({'_id': user['_id']}, {"$set": n_user}, upsert=False)
    return jsonify({'user': n_user})


@app.route('/api/users/<user_name>/', methods=['DELETE'])
def delete_user(user_name):
    user = users.find_one({"username": user_name})
    if len(user) == 0:
        abort(404)
    users.remove(user)
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)
