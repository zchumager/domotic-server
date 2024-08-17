import json
import threading
import os

from datetime import datetime, timedelta

from utils.network import get_connected_macs
from utils.models import session
from utils.crud import get_active_devices_by_timestamp, get_registered_devices, get_active_devices
from utils.climate import calculate_with_model, get_ac_state, change_temperature

base_dir = os.path.abspath(os.path.dirname(__file__))


def logfile_path():
    return os.path.join(base_dir, 'active_devices.log')


def get_registered_connected_macs():
    # list of active devices on network based on an active session using timestamp
    return [device.partial_mac for device in get_active_devices_by_timestamp()]


def wait_for_registered_connected_macs(seconds_timeout=30):
    """""
    Get devices in the network that are registered into utils/app.db
    
    Important note: This method is deprecated since it was replaced by the method above
    get_registered_connected_devices.
    
    The reason for the deprecation of this function is because of the creation 
    of an intersection set between registered_macs and connected_macs by NMAP
    sometimes returns an empty list.
    In other words NMAP  is not always returning a list of registered_connected_macs
    due to network flakiness, but the code is being conserved because
    this was the first approach to define active devices on network.
    """""

    registered_macs = [registered_device.partial_mac for registered_device in get_registered_devices()]
    connected_macs = [mac[3:] for mac in get_connected_macs()]

    # intersection to get connected devices that has been registered
    registered_connected_macs = get_active_devices(connected_macs)
    timeout = datetime.now() + timedelta(seconds=seconds_timeout)

    '''
    timeout for mitigating WiFi intermitences 
    to force finding registered devices that are connected to the network
    '''
    if not len(get_active_devices(connected_macs)):
        while not len(registered_connected_macs) and datetime.now() <= timeout:
            connected_macs = [mac[3:] for mac in get_connected_macs()]
            registered_connected_macs = list(set(registered_macs) & set(connected_macs))
    else:
        registered_connected_macs = list(set(registered_macs) & set(connected_macs))

    return registered_connected_macs


def job():
    print("watching for active devices")

    '''
    active_devices_mac list is used to write active_devices.log file and
    active_devices list is used to change the temperature
    '''
    registered_connected = get_registered_connected_macs()

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
                desired_temperature = calculate_with_model(get_active_devices(registered_connected))
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
            desired_temperature = calculate_with_model(get_active_devices(registered_connected))

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
    os.popen(r'crontab -l | sed "/^[^#].*\/home\/admin\/Repos\/domotic-server\/venv\/bin\/python \/home\/admin\/Repos\/domotic-server\/cronjob.py/s/^/#/" | sudo crontab -').close()
    return "cronjob deactivated"


def activate_cronjob():
    # sudo is not needed when flask or guinicorn is being run with sudo privileges
    os.popen(r'crontab -l | sed "/^#.*\/home\/admin\/Repos\/domotic-server\/venv\/bin\/python \/home\/admin\/Repos\/domotic-server\/cronjob.py/s/^#//" | sudo crontab -').close()
    return "cronjob activated"


if __name__ == "__main__":
    t = threading.Thread(target=job)
    t.start()
