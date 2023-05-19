from flask import Flask, g, make_response, request, jsonify
import sqlite3, random, string

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# CORS
from flask_cors import CORS
CORS(app, resources={r'/api/*': {'origins': '*', 'supports_credentials': True}})

# Database

def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect('db/belay.sqlite3')
        db.row_factory = sqlite3.Row
        setattr(g, '_database', db)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    db.commit()
    cur.close()
    if rv:
        if one:
            return rv[0]
        else:
            return rv
    return None

# Helper Functions

def new_user(username, password):
    api_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=40))
    u = query_db('insert into users (name, password, api_key) ' + 
        'values (?, ?, ?) returning id, name, password, api_key',
        (username, password, api_key),
        one=True)
    return u

def require_api_key(func):
    def decorated_function(*args, **kwargs):
        api_key = request.cookies.get('api_key')
        if not api_key:
            return jsonify({'error': 'No api_key found'}), 401
        user = query_db('select * from users where api_key = ?', (api_key,), one=True)

        if not user:
            return jsonify({'error': 'Invalid api_key'}), 401
        
        return func(*args, **kwargs)
    
    decorated_function.__name__ = func.__name__
    return decorated_function

# API Routes

# Auth

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    user = new_user(username, password)

    channels = query_db('select * from channels')
    if channels:
        for channel in channels:
            query_db('insert into last_read_messages (user_id, channel_id, message_id) values (?, ?, ?)', (user['id'], channel['id'], 0))

    resp = make_response()
    resp.status = 201
    resp.set_cookie('api_key', user['api_key'])
    return resp

@app.route('/api/auth/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = query_db('select * from users where name = ? and password = ?', (username, password), one=True)
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401
    resp = make_response()
    resp.status = 200
    resp.set_cookie('api_key', user['api_key'])
    return resp

@app.route('/api/auth/logout', methods=['POST'])
@require_api_key
def logout():
    resp = make_response()
    resp.status = 200
    resp.set_cookie('api_key', '', expires=0)
    return resp

# Users

@app.route('/api/users/me', methods=['GET'])
@require_api_key
def me():
    api_key = request.cookies.get('api_key')
    user = query_db('select * from users where api_key = ?', (api_key,), one=True)
    return jsonify({'username': user['name']}), 200

@app.route('/api/users/username/update', methods=['PUT'])
@require_api_key
def update_username():
    api_key = request.cookies.get('api_key')
    user = query_db('select * from users where api_key = ?', (api_key,), one=True)
    new_username = request.json.get('username')
    query_db('update users set name = ? where id = ?', (new_username, user['id']))
    return jsonify({'username': new_username}), 200

@app.route('/api/users/password/update', methods=['PUT'])
@require_api_key
def update_password():
    api_key = request.cookies.get('api_key')
    user = query_db('select * from users where api_key = ?', (api_key,), one=True)
    new_password = request.json.get('password')
    query_db('update users set password = ? where id = ?', (new_password, user['id']))
    return jsonify({'password': new_password}), 200

# Channels

@app.route('/api/channels/create', methods=['POST'])
@require_api_key
def create_channel():
    channel_name = request.json.get('channel_name')
    query_db('insert into channels (name) values (?)', (channel_name,))

    channel = query_db('select * from channels where name = ?', (channel_name,), one=True)
    users = query_db('select * from users')
    for user in users:
        query_db('insert into last_read_messages (user_id, channel_id, message_id) values (?, ?, ?)', (user['id'], channel['id'], 0))

    return jsonify({'channel_name': channel_name}), 201

@app.route('/api/channels/all', methods=['GET'])
@require_api_key
def get_channels():
    channels = query_db('select * from channels')
    return jsonify([dict(channel) for channel in channels]), 200

@app.route('/api/channels/<int:channel_id>/messages', methods=['GET'])
@require_api_key
def get_messages(channel_id):
    messages = query_db('select * from messages where channel_id = ?', (channel_id,))
    return jsonify([dict(message) for message in messages]), 200

@app.route('/api/channels/<int:channel_id>/messages/create', methods=['POST'])
@require_api_key
def create_message(channel_id):
    api_key = request.cookies.get('api_key')
    user = query_db('select * from users where api_key = ?', (api_key,), one=True)
    message = request.json.get('message')
    query_db('insert into messages (user_id, channel_id, message) values (?, ?, ?)', (user['id'], channel_id, message))
    return jsonify({'message': message}), 201

# Messages

@app.route('/api//messages/<int:message_id>/reply', methods=['POST'])
@require_api_key
def reply_message(message_id):
    api_key = request.cookies.get('api_key')
    user = query_db('select * from users where api_key = ?', (api_key,), one=True)
    message = query_db('select * from messages where id = ?', (message_id,), one=True)
    channel_id = message['channel_id']
    reply_message = request.json.get('message')
    query_db('insert into messages (user_id, channel_id, message, reply_to) values (?, ?, ?, ?)', (user['id'], channel_id, reply_message, message_id))
    return jsonify({'message': message}), 201

@app.route('/api/messages/<int:message_id>/replies', methods=['GET'])
@require_api_key
def get_replies(message_id):
    replies = query_db('select * from messages where reply_to = ?', (message_id,))
    return jsonify([dict(reply) for reply in replies]), 200

@app.route('/api/messages/<int:message_id>/reactions/create', methods=['POST'])
@require_api_key
def create_reaction(message_id):
    api_key = request.cookies.get('api_key')
    user = query_db('select * from users where api_key = ?', (api_key,), one=True)
    emoji = request.json.get('emoji')
    query_db('insert into reactions (user_id, message_id, emoji) values (?, ?, ?)', (user['id'], message_id, emoji))
    return jsonify({'emoji': emoji}), 201

@app.route('/api/messages/<int:message_id>/reactions', methods=['GET'])
@require_api_key
def get_reactions(message_id):
    reactions = query_db('select * from reactions where message_id = ?', (message_id,))
    return jsonify([dict(reaction) for reaction in reactions]), 200

# Last Read

@app.route('/api/users/<int:user_id>/channels/<int:channel_id>/last', methods=['POST'])
@require_api_key
def update_last_read(user_id, channel_id):
    message_id = request.json.get('message_id')
    query_db('insert into last_read_messages (user_id, channel_id, message_id) values (?, ?, ?)', (user_id, channel_id, message_id))
    return jsonify({'message_id': message_id}), 201

@app.route('/api/users/<int:user_id>/channels/<int:channel_id>/last', methods=['GET'])
@require_api_key
def get_last_read(user_id, channel_id):
    last_read_message = query_db('select * from last_read_messages where user_id = ? and channel_id = ?', (user_id, channel_id), one=True)
    return jsonify({'message_id': last_read_message['message_id']}), 200

@app.route('/api/users/<int:user_id>/channels/<int:channel_id>/unread', methods=['GET'])
@require_api_key
def get_unread_count(user_id, channel_id):
    # YOU MUST USE ONLY ONE QUERY
    unread_count = query_db('select count(*) from messages where channel_id = ? and id > (select message_id from last_read_messages where user_id = ? and channel_id = ?)', (channel_id, user_id, channel_id), one=True)
    return jsonify({'unread_count': unread_count[0]}), 200


if __name__ == '__main__':
    app.run()