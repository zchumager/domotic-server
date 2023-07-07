import json
import threading
import os
import config

from datetime import datetime, timedelta

from utils.network import get_connected_devices
from utils.models import session
from utils.crud import get_active_devices_by_timestamp, get_registered_devices, get_active_devices
from utils.climate import calculate_with_model, get_ac_state, change_temperature

base_dir = os.path.abspath(os.path.dirname(__file__))


def logfile_path():
    return os.path.join(base_dir, 'active_devices.log')


def wait_for_registered_connected_devices(seconds_timeout=30):
    """""
    Get devices in the network that are registered into utils/app.db
    """""

    registered_devices = [registered_device.partial_mac for registered_device in get_registered_devices()]
    connected_devices = [device[3:] for device in get_connected_devices()]

    # intersection to get connected devices that has been registered
    registered_connected = get_active_devices(connected_devices)
    timeout = datetime.now() + timedelta(seconds=seconds_timeout)

    '''
    timeout for mitigating WiFi intermitences 
    to force finding registered devices that are connected to the network
    '''
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
    registered_connected = get_active_devices_by_timestamp()

    logfile = logfile_path()
    update_log = False

    # creates the log file if not exists
    if not os.path.exists(logfile):
        print("Creating active devices log file for cronjob")
        with open(logfile, 'w') as log:
            json.dump(registered_connected, log)

    # checks if the active devices in network have changed
    print("Reading active devices log")
    with open(logfile, 'r') as log:
        macs_in_file = json.loads(log.readline())
        if macs_in_file != registered_connected:
            print("Devices list have change")
            update_log = True
        else:
            print("there are not new devices from previous scan")

    # updates the log file
    if update_log:
        with open(logfile, 'w') as log:
            json.dump(registered_connected, log)

            if len(registered_connected) > 0:
                desired_temperature = calculate_with_model(get_active_devices(registered_connected), model=config.climate_model)
                response = change_temperature(desired_temperature)

                if response.ok:
                    print(f"The new temperature is {desired_temperature}")
                else:
                    print("The temperature could not be modified")
            else:
                print("There are no users connected")
    else:
        if len(registered_connected) > 0:
            ac_state = get_ac_state()
            desired_temperature = calculate_with_model(get_active_devices(registered_connected),
                                                       model=config.climate_model)

            current_temperature = ac_state.json()['attributes']['temperature']

            if current_temperature != desired_temperature:
                response = change_temperature(desired_temperature)

                if response.ok:
                    print(f"The new temperature is {desired_temperature}")
                else:
                    print("The temperature could not be modified")
        else:
            print("There are no users connected")

    session.remove()


def get_cronjob():
    # sudo is not needed when flask or guinicorn is being run with sudo privileges
    execution = os.popen('crontab -l | grep cronjob.py')
    output = execution.read()
    execution.close()
    return output


def deactivate_cronjob():
    # sudo is not needed when flask or guinicorn is being run with sudo privileges
    os.popen('crontab -l | sed "/^[^#].*\/home\/admin\/Repos\/domotic-server\/venv\/bin\/python \/home\/admin\/Repos\/domotic-server\/cronjob.py/s/^/#/" | sudo crontab -').close()
    return "cronjob deactivated"


def activate_cronjob():
    # sudo is not needed when flask or guinicorn is being run with sudo privileges
    os.popen('crontab -l | sed "/^#.*\/home\/admin\/Repos\/domotic-server\/venv\/bin\/python \/home\/admin\/Repos\/domotic-server\/cronjob.py/s/^#//" | sudo crontab -').close()
    return "cronjob activated"


if __name__ == "__main__":
    t = threading.Thread(target=job)
    t.start()
