import itertools
from utils.models import session, Device


def get_registered_devices():
    devices = session.query(Device).all()
    return devices


def get_registered_device(partial_mac):
    # session from models file
    device = session.query(Device).filter(Device.partial_mac == partial_mac).first()
    return device


def get_active_devices(macs):
    active_devices = session.query(Device).filter(Device.partial_mac.in_(macs)).all()
    return active_devices


def update_role(partial_mac, role):
    device = get_registered_device(partial_mac)
    device.role = role
    return device.role

