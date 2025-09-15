from enum import Enum
from typing import TypeAlias, NamedTuple

# DHT22 sensor conntected to GPIO12 as per instructions
# Feel free to pick a different GPIO PIN
DEFAULT_PIN = 12

class DHTSensor(Enum):
    """Use: `sensor: int = DHTSensor.DHT22.value`"""
    DHT11 = 11
    DHT22 = 22
    AM2302 = 22


class DHTSensorConfig(NamedTuple):
    sensor: int
    pin: int


def get_dht_sensor(
        sensor: DHTSensor = DHTSensor.DHT22,
        pin: int = DEFAULT_PIN,
        max_gpio_pins: int = 31
    ) -> DHTSensorConfig:
    if pin < 0 or pin > max_gpio_pins:
        raise ValueError(f"GPIO PIN MAX is {max_gpio_pins}. Pick a vaid GPIO pin number. {pin=}")
    return DHTSensorConfig(sensor.value, pin)
