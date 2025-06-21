import config
from utils import climate_model
from requests import get, post


def calculate_with_model(active_devices):
    print("Calculating Temperature")
    print("Calculating temperature with climate_model")
    return climate_model.execute(active_devices)


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
