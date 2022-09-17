import json
import threading
import os

from utils.network import get_connected_devices
from utils.models import session
from utils.crud import get_registered_devices, get_active_devices
from utils.climate import change_temperature

base_dir = os.path.abspath(os.path.dirname(__file__))


def logfile_path():
    return os.path.join(base_dir, 'active_devices.log')


def get_active_devices_macs():
    connected_devices = get_connected_devices()
    registered_devices = get_registered_devices()

    # getting connected devices from API
    connected_devices_macs = [device[3:] for device in connected_devices]
    registered_devices_macs = [device.partial_mac.upper() for device in registered_devices]

    active_devices_macs = list(set(connected_devices_macs) & set(registered_devices_macs))

    return active_devices_macs


def job():
    print("watching")

    active_devices_macs = get_active_devices_macs()
    active_devices = get_active_devices(active_devices_macs)

    logfile = logfile_path()
    update_log = False

    # creates the log file if not exists
    if not os.path.exists(logfile):
        print("Creating active devices log file for cronjob")
        with open(logfile, 'w') as log:
            json.dump(active_devices_macs, log)
            change_temperature(active_devices)

    # checks if the active devices in network have changed
    print("Reading active devices log")
    with open(logfile, 'r') as log:
        macs_in_file = json.loads(log.readline())
        if macs_in_file != active_devices_macs:
            print("Devices list have change")
            update_log = True

        else:
            print("there are not new devices from previous scan")

    # updates the log file
    if update_log:
        with open(logfile, 'w') as log:
            json.dump(active_devices_macs, log)
            change_temperature(active_devices)

    session.remove()


if __name__ == "__main__":
    t = threading.Thread(target=job)
    t.start()
