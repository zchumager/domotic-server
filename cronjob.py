import json
import threading
import requests
import os


def job():
    print("watching")

    connected_devices = requests.get("http://192.168.1.8:5000/connected_devices")
    if not connected_devices.ok:
        connected_devices = []

    # getting connected devices from API
    connected_devices = connected_devices.json()

    logfile = os.path.abspath('./domotic-cronjob.log')
    with open(logfile, 'w') as log:
        json.dump(connected_devices, log)


if __name__ == "__main__":
    t = threading.Thread(target=job)
    t.start()
