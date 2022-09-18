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


def get_active_devices_macs():
    """
    :return: the list of mac_addresses in db that are currently active in the wifi
    """

    connected_devices = get_connected_devices()
    registered_devices = get_registered_devices()

    # getting connected devices from API
    connected_devices_macs = [device[3:] for device in connected_devices]
    registered_devices_macs = [device.partial_mac.upper() for device in registered_devices]

    # intersection to get connected devices that has been registered
    active_devices_macs = list(set(connected_devices_macs) & set(registered_devices_macs))

    return active_devices_macs


def get_active_devices_info():
    """
    returns the list of the active devices' mac address and
    the list of devices in db that are currently active in the wifi
    """

    active_devices_macs = get_active_devices_macs()
    active_devices = get_active_devices(active_devices_macs)

    return active_devices_macs, active_devices


def wait_for_connected_devices(fn=get_active_devices_info, seconds_timeout=30):
    """""
    this function was done to mitigate wifi intermitences
    """""

    active_devices_macs, active_devices = fn()

    stop_time = datetime.now() + timedelta(seconds=seconds_timeout)

    while len(active_devices) == 0 and datetime.now() <= stop_time:
        time.sleep(seconds_timeout)

        active_devices_macs, active_devices = fn()

    return active_devices_macs, active_devices


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
