import os

from flask import Flask, send_from_directory, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

from utils.network import get_connected_devices
from utils.crud import get_registered_device, get_registered_devices

from utils.models import session, Device, device_schema

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
    return '<h1>REST API</h1>'


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
        return jsonify(msg='bad request not registered device')

    if registered_device.role == "visitor":
        return jsonify(msg='a visitor cannot an access token')

    access_token = create_access_token(identity=partial_mac)
    return jsonify(access_token=access_token), 200


@app.route("/join2home", methods=["POST"])
def join2home():
    body = request.get_json()
    partial_mac = body.get('partial_mac', None)
    user = get_registered_device(partial_mac)

    if user is None:
        email = body.get('email', None)
        firstname = body.get('firstname', None)
        lastname = body.get('lastname', None)

        desired_temperature = body.get('desired_temperature', None)
        is_sick = body.get('is_sick', None)
        medical_condition_level = body.get('medical_condition_level', None)

        registered_devices = get_registered_devices()

        if not len(registered_devices):
            role = "habitant"
        else:
            role = "visitor"

        device = Device(
            partial_mac=partial_mac,
            email=email,
            firstname=firstname,
            lastname=lastname,
            role=role,
            desired_temperature=desired_temperature,
            is_sick=is_sick,
            medical_condition_level=medical_condition_level
        )

        session.add(device)
        session.commit()

        if device.id is None:
            return jsonify(msg="device could not be registered"), 409

        return jsonify(body), 200
    else:
        return jsonify(msg="this is already registered"), 409


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
