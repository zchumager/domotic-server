import os

from flask import Flask, send_from_directory, jsonify, request, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from utils.crud import update_expiration_timestamp, get_registered_device, get_registered_devices, update_role
from utils.models import session, Device
from utils.network import get_connected_macs, get_server_ip
from cronjob import get_registered_connected_devices, get_cronjob, activate_cronjob, deactivate_cronjob

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JWT_SECRET_KEY'] = 'domotic_server_secret_key'
jwt = JWTManager(app)


static_folder = os.path.join(app.root_path, 'static')


@app.route('/')
def index():
    ip = get_server_ip()
    return render_template("index.html", ip_address=ip)


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
        return jsonify(msg='bad request not registered device'), 404

    if registered_device.role == "visitor":
        access_token = create_access_token(identity=registered_device.role)
        return jsonify(access_token=access_token, role="visitor"), 200

    access_token = create_access_token(identity=partial_mac)
    return jsonify(access_token=access_token, role="habitant"), 200


@app.route("/join2home", methods=["POST"])
def join2home():
    body = request.get_json()
    partial_mac = body.get('partial_mac', None)
    if partial_mac is None:
        return jsonify(msg="bad Request for joining to the family"), 400

    registered_device = get_registered_device(partial_mac)

    if registered_device is not None:
        return jsonify(msg="this is already registered"), 409

    device_name = body.get('device_name', None)
    email = body.get('email', None)
    firstname = body.get('firstname', None)
    lastname = body.get('lastname', None)

    desired_temperature = body.get('desired_temperature', None)
    medical_condition = body.get('medical_condition', None)
    medical_condition_level = body.get('medical_condition_level', None) if medical_condition else ""

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


@app.route("/join2family", methods=["POST"])
@jwt_required()
def join2family():
    body = request.get_json()

    habitant_partial_mac = body.get('habitant_partial_mac', None)
    visitor_partial_mac = body.get('visitor_partial_mac', None)

    if habitant_partial_mac is None or visitor_partial_mac is None:
        return jsonify(msg="bad Request for joining to the family"), 400

    identy = get_jwt_identity()

    if identy == "visitor":
        return jsonify(msg="forbiden service for visitors"), 403

    habitant_device = get_registered_device(habitant_partial_mac)

    if habitant_device is None:
        return jsonify(msg='bad request habitant not registered'), 404

    new_role = update_role(visitor_partial_mac, habitant_device.role)

    return jsonify(msg=f"role updated to {new_role}")


@app.route("/device_info")
def device_info():
    partial_mac = request.args.get('partial_mac', "")

    partial_mac = partial_mac.replace('"', '')

    registered_device = get_registered_device(partial_mac)

    if registered_device is None:
        return jsonify(msg='bad request not registered device'), 404

    info = {
        'email': registered_device.email,
        'firstname': registered_device.firstname,
        'lastname': registered_device.lastname,
        'desired_temperature': registered_device.desired_temperature,
        'medical_condition': registered_device.medical_condition,
        'medical_condition_level': registered_device.medical_condition_level
    }

    return jsonify(info), 200


@app.route("/update_expiration", methods=["PUT"])
def update_expiration():
    body = request.get_json()
    partial_mac = body.get('partial_mac', None)
    if partial_mac is None:
        return jsonify(msg="bad Request for updating expiration"), 400

    new_timestamp = update_expiration_timestamp(partial_mac)

    return jsonify(new_timestamp), 201


@app.route("/update_preferences", methods=["PUT"])
@jwt_required()
def update_preferences():
    body = request.get_json()
    partial_mac = body.get('partial_mac', None)
    if partial_mac is None:
        return jsonify(msg="bad Request for joining to the family"), 400

    device = get_registered_device(partial_mac)

    if device is None:
        return jsonify(msg='bad request not registered device'), 404

    device.email = body.get('email', None)
    device.firstname = body.get('firstname', None)
    device.lastname = body.get('lastname', None)
    device.desired_temperature = body.get('desired_temperature', None)
    device.medical_condition = body.get('medical_condition', None)
    device.medical_condition_level = body.get('medical_condition_level', None) if device.medical_condition else ""

    session.commit()

    return jsonify(body), 201


@app.route("/all_connected_macs")
@jwt_required()
def all_devices():
    identity = get_jwt_identity()

    if identity == 'visitor':
        return jsonify(msg="any visitor cannot list connected devices"), 401

    return jsonify(get_connected_macs()), 200


@app.route("/registered_connected_macs")
@jwt_required()
def registered_connected():
    identity = get_jwt_identity()

    if identity == 'visitor':
        return jsonify(msg="any visitor cannot list active devices"), 401

    mac_addresses = get_registered_connected_devices()

    return jsonify(mac_addresses), 200


@app.route("/get_cronjob")
def get_cronjob_status():
    return jsonify(get_cronjob()), 200


@app.route("/crontab")
@jwt_required()
def enable_crontab():
    identity = get_jwt_identity()

    if identity == 'visitor':
        return jsonify(msg="any visitor cannot activate crontab"), 401

    return jsonify(activate_cronjob()), 200


@app.route("/quitcron")
@jwt_required()
def deactivate_crontab():
    identity = get_jwt_identity()

    if identity == 'visitor':
        return jsonify(msg="any visitor cannot deactivate crontab"), 401

    return jsonify(deactivate_cronjob()), 200


@app.teardown_request
def remove_session(ex=None):
    session.remove()


if __name__ == "__main__":
    print("BACKEND REST API")
    app.run(host='0.0.0.0')
