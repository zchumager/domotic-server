import config
from utils import climate_model


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


def change_with_model(active_devices, model=config.climate_model):
    temperatures = []
    weights = []

    for device in active_devices:
        temperatures.append(device.desired_temperature)
        weights.append(get_weight_from_device(device))

    if model == "basic":
        print("Calculating temperature with basic model")

        return climate_model.basic(temperatures, weights)


def change_temperature(active_devices):
    print("Changing Temperature")

    return change_with_model(active_devices, model="basic")


