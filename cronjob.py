import json
import platform
import threading
import os

from utils.network import get_connected_devices


def logfile_path():
    if platform.system() == 'Windows':
        return os.path.abspath('./domotic-cronjob.log')
    elif platform.system() == 'Linux':
        return '/home/admin/Repos/domotic-server/domotic-cronjob.log'


def job():
    print("watching")

    # getting connected devices from API
    connected_devices = get_connected_devices()

    logfile = logfile_path()
    if os.path.exists(logfile):
        print("Comparing connected users with log file")
    else:
        print("Creating log file with connected users")
        with open(logfile, 'w') as log:
            json.dump(connected_devices, log)


if __name__ == "__main__":
    t = threading.Thread(target=job)
    t.start()
