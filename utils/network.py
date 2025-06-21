import platform
import nmap
import socket
import pprint

from xml.etree.ElementTree import ParseError


def get_server_ip():
    skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    skt.connect(("8.8.8.8", 80))

    return skt.getsockname()[0]


def get_connected_macs():
    print("Getting Connected Devices")

    server_ip = get_server_ip()
    print(f'Server IP: {server_ip}')
    network_segment = f'{server_ip}/24'
    mac_addresses = []

    try:
        if platform.system() == 'Windows':
            nmap_path = [r"C:\Program Files (x86)\Nmap\nmap.exe"]
            nm_scanner = nmap.PortScanner(nmap_search_path=nmap_path)
        elif platform.system() == 'Linux':
            nm_scanner = nmap.PortScanner()
    except nmap.PortScannerError as e:
        print(e.value)

    try:
        network = nm_scanner.scan(network_segment, arguments='-snP')
        connected_devices = network['scan']

        mac_addresses = [
            device[1].get('addresses').get('mac')
            for device in connected_devices.items()
            if device[1].get('addresses').get('mac') is not None
        ]
    except ParseError as e:
        pprint.pprint(e.msg)

    return mac_addresses
