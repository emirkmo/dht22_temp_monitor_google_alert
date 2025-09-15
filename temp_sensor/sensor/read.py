from typing import Any, NamedTuple
import logging
import time

import Adafruit_DHT # type: ignore
from .physical_config import DHTSensorConfig

class Reading(NamedTuple):
    timestamp: int
    temperature: float
    humidity: float | None

def read_sensor(sensor_config: DHTSensorConfig) -> Reading | None:
    humidity, temperature = Adafruit_DHT.read_retry(sensor_config.sensor, sensor_config.pin)
    timestamp = int(time.time())
    return format_vals(humidity=humidity, temperature=temperature, timestamp=timestamp)


def format_vals(humidity: Any, temperature: Any, timestamp: int) -> Reading | None:
    if temperature is None:
        return None
    try:
        temp_c = float(f"{temperature:0.1f}")
    except (ValueError, TypeError) as err:
        logging.error(err)
        return None

    try:
        humidity_percent = float(f"{humidity:0.1f}")
    except (ValueError, TypeError) as err:
        logging.error(err)
        humidity_percent = None
    if timestamp < 0:
        return None
    return Reading(timestamp, temp_c, humidity_percent)

