from db import *
from app import *
from flask import request, session, abort, Response, jsonify, render_template
import json
from datetime import datetime


def create_user(type, name, username, email, picture):
    users = json.loads(User.objects().to_json())
    try:
        u_id = users[0]["user_id"]+1
    except:
        u_id = 1
    user = User(user_id=u_id,
                username=username,
                name=name,
                picture=picture,
                email=email,
                type=type,
                bio="",
                location="",
                native="",
                first_login=datetime.now().strftime('%Y-%m-%d'),
                words=[])

    user.save()
    return str(user)


@app.route('/api/user', methods=['GET'])
def get_user():
        user = User.objects(username=session['username'])
        user_json = json.loads(user.to_json())
        return Response(json.dumps(user_json, sort_keys=False, indent=4),mimetype='application/json')


@app.route('/api/user', methods=['PUT'])
def update_user():
    user = User.objects(username=session['username'])
    user.update(**{
            "set__bio": request.json['bio'],
            "set__location": request.json['location'],
            "set__native": request.json['native']})
    user_json = json.loads(user.to_json())
    return Response(json.dumps(user_json, sort_keys=False, indent=4),
                    mimetype='application/json')


@app.route('/api/user', methods=['DELETE'])
def delete_user(username):
    user = User.objects(username=session['username'])
    user_json = json.loads(user.to_json())
    if user_json == []:
        abort(404)
    else:
        user.delete()
        return "ok"
