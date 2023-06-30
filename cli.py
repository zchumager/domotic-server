import argparse
import pprint
from utils.network import get_connected_devices
from cronjob import wait_for_registered_connected_devices, activate_cronjob, deactivate_cronjob

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Server Command Line Interface")

    parser.add_argument('-a', '--all_devices',
                        help="List the MAC Addresses of network's connected devices",
                        action="store_true")

    parser.add_argument('-r', '--registered_connected',
                        help="List of the Mac Addresses of connected devices that are registered in the DB",
                        action="store_true")

    parser.add_argument('-c', '--crontab', help="activate crontab", action="store_true")

    parser.add_argument('-q', '--quitcron', help="deactivate crontab", action="store_true")

    args = parser.parse_args()

    if args.all_devices:
        pprint.pprint(get_connected_devices())
    if args.registered_connected:
        registered_connected = wait_for_registered_connected_devices()
        pprint.pprint(registered_connected)
    if args.crontab:
        pprint.pprint(activate_cronjob())
    if args.quitcron:
        pprint.pprint(deactivate_cronjob())
