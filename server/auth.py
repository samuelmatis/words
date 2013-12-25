from app import *
from users import *
from flask import session, redirect, url_for
from flask.sessions import *
from json import JSONEncoder

@app.route('/api/session', methods=['GET'])
def session_get():
    out = JSONEncoder().encode({
        "username": session['username'],
        "access_token": session['access_token'],
        "fullname": session['name']
    })
    decoded = json.loads(out)
    return Response(json.dumps(decoded, sort_keys=False, indent=4),mimetype='application/json')

@app.route('/api/login/facebook', methods=['POST'])
def login_fb():
    return create_user("facebook", request.json['name'], request.json['username'], request.json['email'], request.json['picture']['data']['url'])

@app.route('/api/login/twitter', methods=['POST'])
def login_tw():
    pass


@app.route('/api/login/google', methods=['POST'])
def login_plus():
    pass

@app.route('/api/logout', methods=['GET'])
def logout():
    session.pop('access_token', None)
    return redirect(url_for('index'))
