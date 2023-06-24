import json
import threading
import os
import time

from datetime import datetime, timedelta

from utils.network import get_connected_devices
from utils.models import session
from utils.crud import get_registered_devices, get_active_devices
from utils.climate import change_temperature

base_dir = os.path.abspath(os.path.dirname(__file__))


def logfile_path():
    return os.path.join(base_dir, 'active_devices.log')


def wait_for_connected_devices(seconds_timeout=30):
    """""
    this function was done to mitigate wifi intermitences
    """""

    registered_devices = [registered_device.partial_mac for registered_device in get_registered_devices()]
    connected_devices = [device[3:] for device in get_connected_devices()]

    # intersection to get connected devices that has been registered
    registered_connected = get_active_devices(connected_devices)
    timeout = datetime.now() + timedelta(seconds=seconds_timeout)

    if not len(get_active_devices(connected_devices)):
        while not len(registered_connected) and datetime.now() <= timeout:
            connected_devices = [device[3:] for device in get_connected_devices()]
            registered_connected = list(set(registered_devices) & set(connected_devices))
    else:
        registered_connected = list(set(registered_devices) & set(connected_devices))

    return registered_connected


def job():
    print("watching for active devices")

    '''
    active_devices_mac list is used to write active_devices.log file and
    active_devices list is used to change the temperature
    '''
    active_devices_macs, active_devices = wait_for_connected_devices()

    logfile = logfile_path()
    update_log = False

    # creates the log file if not exists
    if not os.path.exists(logfile):
        print("Creating active devices log file for cronjob")
        with open(logfile, 'w') as log:
            json.dump(active_devices_macs, log)

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

            if len(active_devices_macs) > 0:
                new_temperature = change_temperature(active_devices)
                print(f"The new temperature is {new_temperature}")

    session.remove()


if __name__ == "__main__":
    t = threading.Thread(target=job)
    t.start()
