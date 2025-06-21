from datetime import datetime, timedelta
from utils.models import session, Device


def get_registered_devices():
    devices = session.query(Device).all()
    return devices


def get_registered_device(partial_mac):
    # session from models file
    device = session.query(Device).filter(Device.partial_mac == partial_mac).first()
    return device


def get_active_devices_by_timestamp():
    """"
    Returns a list of records from Device table with an expiration_timestamp
    greater than the current timestamp obtained with datetime.now()
    """
    devices = session.query(Device).filter(Device.expiration_timestamp >= datetime.now()).all()
    return devices


def get_registered_connected_devices(partial_macs):
    devices = session.query(Device).filter(Device.partial_mac.in_(partial_macs)).all()
    return devices


def update_role(partial_mac, role):
    device = get_registered_device(partial_mac)
    device.role = role
    session.commit()

    return device.role


def update_expiration_timestamp(partial_mac):
    device = get_registered_device(partial_mac)
    device.expiration_timestamp = datetime.now() + timedelta(minutes=2)
    session.commit()

    return device.expiration_timestamp

