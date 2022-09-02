import os

from flask import Flask, send_from_directory, jsonify

from utils.network import get_server_info, get_connected_devices

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    return 'REST API'


@app.route("/about")
def about():
    return jsonify({
        'application': 'REST API Domotic Server',
        'version': 1.0,
        'author': 'Pedro Arnoldo Machado Duran'
    })


@app.route('/server_info')
def server_info():
    return jsonify(get_server_info())


@app.route("/connected_devices")
def connected_devices():
    return jsonify(get_connected_devices())


if __name__ == "__main__":
    print("BACKEND REST API")
    app.run(host='0.0.0.0')
