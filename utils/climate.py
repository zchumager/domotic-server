import config
from utils import climate_model
from requests import get, post


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


def calculate_with_model(active_devices, model):
    print("Changing Temperature")

    temperatures = []
    weights = []

    for device in active_devices:
        temperatures.append(device.desired_temperature)
        weights.append(get_weight_from_device(device))

    if model == "basic":
        print("Calculating temperature with basic model")

        return climate_model.basic(temperatures, weights)


def get_ac_state():
    headers = {
        'Authorization': f'Bearer {config.access_token}'
    }

    hostname = config.raspberry_ip
    endpoint = f"/api/states/{config.entity_id}"

    return get(f"{hostname}{endpoint}", headers=headers)


def change_temperature(temperature):
    headers = {
        'Authorization': f'Bearer {config.access_token}'
    }

    body = {
        "entity_id": f"{config.entity_id}",
        "temperature": temperature,
        "target_temp_high": 26,
        "target_temp_low": 20,
        "hvac_mode": "cool"
    }

    hostname = config.raspberry_ip
    endpoint = "/api/services/climate/set_temperature"

    return post(f"{hostname}{endpoint}", json=body, headers=headers)
