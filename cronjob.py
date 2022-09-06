import json
import threading
import os

from utils.network import get_connected_devices
from utils.models import session
from utils.crud import get_registered_devices, get_active_devices

base_dir = os.path.abspath(os.path.dirname(__file__))


def logfile_path():
    return os.path.join(base_dir, 'active_devices.log')


def job():
    print("watching")

    connected_devices = get_connected_devices()
    registered_devices = get_registered_devices()

    # getting connected devices from API
    connected_devices_macs = [device[3:] for device in connected_devices]
    registered_devices_macs = [device.partial_mac.upper() for device in registered_devices]

    active_devices_macs = list(set(connected_devices_macs) & set(registered_devices_macs))

    active_devices = get_active_devices(active_devices_macs)

    logfile = logfile_path()
    if os.path.exists(logfile):
        print("Comparing connected users with log file")

        with open(logfile, 'w') as log:
            json.dump(active_devices_macs, log)
    else:
        print("Creating log file with connected users")
        with open(logfile, 'w') as log:
            json.dump(active_devices_macs, log)

    session.remove()


if __name__ == "__main__":
    t = threading.Thread(target=job)
    t.start()
