from functools import reduce
from operator import add, mul


def get_weight_from_device(device):
    if device.role == 'visitor':
        if not device.medical_condition:
            return 2
        else:
            if device.medical_condition_level == "ESTABLE":
                return 4
            if device.medical_condition_level == "SERIO":
                return 6
            if device.medical_condition_level == "GRAVE":
                return 8
    elif device.role == 'habitant':
        if not device.medical_condition:
            return 3
        else:
            if device.medical_condition_level == "ESTABLE":
                return 5
            if device.medical_condition_level == "SERIO":
                return 7
            if device.medical_condition_level == "GRAVE":
                return 9


def execute(active_devices):
    """
    :param active_devices: list of devices
    :return: the calculated temperature with the model
    """

    print("Executing climate model")

    temperatures = []
    weights = []

    for device in active_devices:
        temperatures.append(device.desired_temperature)
        weights.append(get_weight_from_device(device))

    """
        Summation of multiplication of temperature * weight
    """
    dividend = reduce(add, map(mul, temperatures, weights))
    divisor = sum(weights)

    return dividend // divisor
