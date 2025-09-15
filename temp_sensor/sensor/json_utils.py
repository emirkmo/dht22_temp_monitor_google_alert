from typing import TypedDict, Iterable
from pathlib import Path
import json
import sqlite3


from .read import read_sensor
from .physical_config import DHTSensorConfig
from .default_db import DEFAULT_DB

def print_json(dht_sensor_config: DHTSensorConfig):
    """Continually print json"""
    while True:
        reading = read_sensor(dht_sensor_config)
       
        if not reading:
            continue

        print(json.dumps(
            {"timestamp": reading.timestamp, "temperature": reading.temperature, "humidity": reading.humidity}
        ))

class JSONTemps(TypedDict):
    timestamp: int
    temperature: float
    humidity: float | None

def get_last_x(db_path: Path = DEFAULT_DB, limit: int = 24) -> Iterable[JSONTemps]:
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


