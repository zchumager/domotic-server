import platform
import pythoncom
import nmap

from who_is_on_my_wifi import device


def get_server_info():
    pythoncom.CoInitialize()

    return device()


def get_server_ip():
    return get_server_info()[4]


def get_modem_ip():
    return get_server_info()[8]


def get_connected_devices():
    server_ip = get_server_ip()

    network_segment = f'{server_ip}/24'
    if platform.system() == 'Windows':
        nmap_path = [r"C:\Program Files (x86)\Nmap\nmap.exe"]
        nm_scanner = nmap.PortScanner(nmap_search_path=nmap_path)
    elif platform.system() == 'Linux':
        nm_scanner = nmap.PortScanner()

    network = nm_scanner.scan(network_segment, arguments='-snP')
    connected_devices = network['scan']

    mac_addresses = [device[1].get('addresses').get('mac')
                     for device in connected_devices.items()
                     if device[1].get('addresses').get('mac') is not None]

    return mac_addresses

