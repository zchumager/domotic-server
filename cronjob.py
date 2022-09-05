import json
import threading
import requests


def job():
    print("watching")

    connected_devices = requests.get("http://192.168.1.8:5000/connected_devices")
    if not connected_devices.ok:
        connected_devices = []

    # getting connected devices from API
    connected_devices = connected_devices.json()
    with open('output.log', 'w') as log:
        json.dump(connected_devices, log)


if __name__ == "__main__":
    t = threading.Thread(target=job)
    t.start()
