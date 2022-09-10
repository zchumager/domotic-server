import os

from flask import Flask, send_from_directory, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

from utils.network import get_connected_devices
from utils.crud import get_registered_device, get_registered_devices
from utils.models import session, Device

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JWT_SECRET_KEY'] = 'domotic_server_secret_key'
jwt = JWTManager(app)

static_folder = os.path.join(app.root_path, 'static')


@app.route('/')
def index():
    return send_from_directory(static_folder, 'index.html')


@app.route('/favicon')
def favicon():
    return send_from_directory(static_folder, 'favicon.ico')


@app.route("/about")
def about():
    return jsonify({
        'application': 'REST API Domotic Server',
        'version': 1.0,
        'author': 'Pedro Arnoldo Machado Duran'
    })


@app.route('/login', methods=['POST'])
def login():
    partial_mac = request.json.get('partial_mac', None)
    registered_device = get_registered_device(partial_mac)

    if registered_device is None:
        return jsonify(msg='bad request not registered device'), 409

    if registered_device.role == "visitor":
        return jsonify(msg='a visitor cannot an access token'), 403

    access_token = create_access_token(identity=partial_mac)
    return jsonify(access_token=access_token), 200


@app.route("/join2home", methods=["POST"])
def join2home():
    body = request.get_json()
    partial_mac = body.get('partial_mac', None)
    user = get_registered_device(partial_mac)

    if user is not None:
        return jsonify(msg="this is already registered"), 409

    device_name = body.get('device_name', None)
    email = body.get('email', None)
    firstname = body.get('firstname', None)
    lastname = body.get('lastname', None)

    desired_temperature = body.get('desired_temperature', None)
    medical_condition = body.get('medical_condition', None)
    medical_condition_level = body.get('medical_condition_level', None)

    registered_devices = get_registered_devices()

    if not len(registered_devices):
        role = "habitant"
    else:
        role = "visitor"

    device = Device(
        partial_mac=partial_mac,
        device_name=device_name,
        email=email,
        firstname=firstname,
        lastname=lastname,
        role=role,
        desired_temperature=desired_temperature,
        medical_condition=medical_condition,
        medical_condition_level=medical_condition_level
    )

    session.add(device)
    session.commit()

    if device.id is None:
        return jsonify(msg="device could not be registered"), 403

    return jsonify(body), 200


@app.route("/connected_devices")
@jwt_required()
def connected_devices():
    return jsonify(get_connected_devices()), 200


@app.teardown_request
def remove_session(ex=None):
    session.remove()


if __name__ == "__main__":
    print("BACKEND REST API")
    app.run(host='0.0.0.0')
