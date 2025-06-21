import argparse
import pprint
from utils.network import get_connected_macs
from cronjob import get_registered_connected_macs, wait_for_registered_connected_macs, activate_cronjob, deactivate_cronjob
"""
    This module allows to test features from cronjob
    
    Note: job method testing is not included since it is the main method 
    that can be tested with the regular execution using the commands below:
    
    > source ./venv/bin/activate
    > python cronjob.py
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Server Command Line Interface")

    parser.add_argument('-a', '--all_connected_macs',
                        help="List the MAC Addresses of network's connected devices",
                        action="store_true")

    parser.add_argument('-r', '--registered_connected_macs',
                        help="List of the Mac Addresses of connected devices that are registered in app.db",
                        action="store_true")

    parser.add_argument('-w', '--wait_for_registered_connected_macs',
                        help="List of the Mac Addresses of connected creating an intersection \
                        between MAC address obtained with NMAP and the registered devices in app.db",
                        action="store_true")

    parser.add_argument('-c', '--crontab', help="activate crontab", action="store_true")

    parser.add_argument('-q', '--quitcron', help="deactivate crontab", action="store_true")

    args = parser.parse_args()

    if args.all_connected_macs:
        pprint.pprint(get_connected_macs())
    if args.registered_connected_macs:
        registered_connected_macs = get_registered_connected_macs()
        pprint.pprint(registered_connected_macs)
    if args.wait_for_registered_connected_macs:
        registered_connected_macs = wait_for_registered_connected_macs()
        pprint.pprint(registered_connected_macs)
    if args.crontab:
        pprint.pprint(activate_cronjob())
    if args.quitcron:
        pprint.pprint(deactivate_cronjob())
