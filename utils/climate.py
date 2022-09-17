import config
from utils import climate_model


def change_temperature(active_devices):
    print("Changing Temperature")

    return climate_model.execute(config.climate_model, active_devices)

