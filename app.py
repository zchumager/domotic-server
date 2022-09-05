import os

from flask import Flask, send_from_directory, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

from utils.network import get_connected_devices

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JWT_SECRET_KEY'] = 'secret-paraphase'
jwt = JWTManager(app)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return 'REST API'


@app.route('/login', methods=['POST'])
def login():
    partial_mac = request.json.get('partial_mac', None)

    if partial_mac != 'e6:8e:2f:2d:a9':
        return jsonify({'msg': 'bad request not registered device'})

    access_token = create_access_token(identity=partial_mac)
    return jsonify(access_token)


@app.route("/about")
def about():
    return jsonify({
        'application': 'REST API Domotic Server',
        'version': 1.0,
        'author': 'Pedro Arnoldo Machado Duran'
    })


@app.route("/connected_devices")
@jwt_required()
def connected_devices():
    return jsonify(get_connected_devices())


if __name__ == "__main__":
    print("BACKEND REST API")
    app.run(host='0.0.0.0')
