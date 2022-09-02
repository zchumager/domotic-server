import argparse
import pprint
from utils.network import get_connected_devices

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Server Command Line Interface")
    parser.add_argument('-d', '--devices'
                        , help="List the MAC Addresses of network's connected devices", action="store_true")

    args = parser.parse_args()

    if args.devices:
        pprint.pprint(get_connected_devices())
