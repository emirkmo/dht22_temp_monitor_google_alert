from .read import read_sensor, Reading
from typing import Iterable, Protocol
from collections import deque
import logging
from pathlib import Path

import time
from .default_db import DEFAULT_DB
from .physical_config import DHTSensorConfig

class BatchWriter(Protocol):
    
    def insert_readings(
        db_path: str | Path,
        readings: Iterable[tuple[int, float, float | None]]
    ) -> None:
        ...

def init_sqlite_writer() -> BatchWriter:
    import sensor_db
    DEFAULT_DB.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_DB.touch(exist_ok=True)
    sensor_db.init_db(DEFAULT_DB)

    return sensor_db


BATCH_SIZE = 24
def write_to_db(dht_sensor_config: DHTSensorConfig, writer: BatchWriter, output_path: str | Path = DEFAULT_DB, sleep_seconds: int | float = 2.5):
    """Read DHT sensor and write data to sqlite every minute, in batches of 60/sleep_seconds entries."""
    batch_size = int(60//sleep_seconds)
    readings: list[Reading] = deque(maxlen=batch_size)
    while True:
        reading = read_sensor(dht_sensor_config)
        if reading:
            readings.append(reading)

        #logging.debug(reading)
        if len(readings) >= batch_size:
            logging.info("latest reading:%s", reading)
            try:
                writer.insert_readings(output_path, readings)
            except Exception as e:
                logging.error(f"DB error inserting batch: {e}")
            readings.clear()        
        time.sleep(sleep_seconds)


