from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify('pong!')

if __name__ == '__main__':
    app.run()