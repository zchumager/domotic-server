import argparse
import pprint
from utils.network import get_connected_devices
from cronjob import wait_for_connected_devices

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Server Command Line Interface")

    parser.add_argument('-d', '--devices',
                        help="List the MAC Addresses of network's connected devices",
                        action="store_true")

    parser.add_argument('-a', '--active_devices',
                        help="List of the Mac Addresses of connected devices that are registered in the DB",
                        action="store_true")

    args = parser.parse_args()

    if args.devices:
        pprint.pprint(get_connected_devices())
    if args.active_devices:
        active_devices_macs, _ = wait_for_connected_devices()
        pprint.pprint(active_devices_macs)
