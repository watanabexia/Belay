from flask import Flask, g, make_response, request, jsonify
from flask_cors import CORS
import sqlite3, random, string

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

CORS(app, resources={r'/api/*': {'origins': '*', 'supports_credentials': True}})

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

def new_user():
    name = "Unnamed User #" + ''.join(random.choices(string.digits, k=6))
    password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    api_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=40))
    u = query_db('insert into users (name, password, api_key) ' + 
        'values (?, ?, ?) returning id, name, password, api_key',
        (name, password, api_key),
        one=True)
    return u

def require_api_key(func):
    def decorated_function(*args, **kwargs):

        print(request.cookies)

        api_key = request.cookies.get('api_key')
        if not api_key:
            return jsonify({'error': 'No api_key found'}), 401
        user = query_db('select * from users where api_key = ?', (api_key,), one=True)

        if not user:
            return jsonify({'error': 'Invalid api_key'}), 401
        
        return func(*args, **kwargs)
    
    decorated_function.__name__ = func.__name__
    return decorated_function

@app.route('/api/auth/signup', methods=['GET'])
def signup():
    user = new_user()
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

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify('pong!')

if __name__ == '__main__':
    app.run()