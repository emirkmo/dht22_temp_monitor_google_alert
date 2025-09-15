import sqlite3
from pathlib import Path
import time
import Adafruit_DHT
from typing import Any
import json

sensor = Adafruit_DHT.DHT22
# DHT22 sensor conntected to GPIO12 as per instructions
pin = 12

DEFAULT_DB = Path("/var/lib/temp_sensor/data.db")

def format_vals(humidity: Any, temperature: Any) -> tuple[float, float | None] | None:
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
    return temp_c, humidity_percent

def print_json():
    """Continually print json"""
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        ts = int(time.time())
        reading = format_vals(humidity, temperature)
        if not reading:
            continue
        temp_c, humidity_percent = reading
        as_float_dict = {"timestamp": ts, "temperature": temp_c, "humidity": humidity_percent}
        print(json.dumps(as_float_dict))

def get_last_x(db_path: Path, limit: int = 24):
    """
    Fetch the `limit` most recent readings and print them as JSON:
      [{"timestamp":…, "temperature":…, "humidity":…}, …]
    """
    with sqlite3.connect(str(db_path)) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT timestamp, temperature, humidity "
            "FROM readings "
            "ORDER BY timestamp DESC "
            f"LIMIT {limit}"
        )
        rows = cur.fetchall()
    for ts, temp, hum in reversed(rows):
        yield {"timestamp": ts, "temperature": temp, "humidity": hum}

if __name__ == '__main__':
   while True:
      for reading in get_last_x(DEFAULT_DB):
        print(reading)

      time.sleep(60)
