import json
import threading
import os

from utils.network import get_connected_devices
from utils.models import session
from utils.crud import get_registered_devices

base_dir = os.path.abspath(os.path.dirname(__file__))


def logfile_path():
    return os.path.join(base_dir, 'connected_users.log')


def job():
    print("watching")

    # getting connected devices from API
    connected_devices = get_connected_devices()
    registered_devices = get_registered_devices()

    logfile = logfile_path()
    if os.path.exists(logfile):
        print("Comparing connected users with log file")
    else:
        print("Creating log file with connected users")
        with open(logfile, 'w') as log:
            json.dump(connected_devices, log)

    session.remove()


if __name__ == "__main__":
    t = threading.Thread(target=job)
    t.start()
