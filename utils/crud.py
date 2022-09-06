from utils.models import session, Device


def get_registered_devices():
    devices = session.query(Device).all()
    return devices


def get_registered_device(partial_mac):
    # session from models file
    device = session.query(Device).filter(Device.partial_mac == partial_mac).first()
    return device
