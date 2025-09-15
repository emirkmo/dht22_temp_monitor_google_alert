from sensor.write import write_to_db, init_sqlite_writer
from sensor.default_db import DEFAULT_DB
from sensor.physical_config import get_dht_sensor
import logging 
import logging.handlers
import sys

def setup_logging():

    # Configure root logger to send to syslog via /dev/log, using the LOCAL0 facility
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    syslog_handler = logging.handlers.SysLogHandler(
        address='/dev/log',
        facility=logging.handlers.SysLogHandler.LOG_LOCAL1
    )
    formatter = logging.Formatter('%(name)s[%(process)d]: %(levelname)s %(message)s')
    syslog_handler.setFormatter(formatter)
    logger.addHandler(syslog_handler)



def main():
    """Continously read sensor & write data to sqlite"""
    setup_logging()
    logging.debug(f"Using DB at: {DEFAULT_DB}", file=sys.stderr)

    try:
        sensor_db = init_sqlite_writer()
        sensor_config = get_dht_sensor()
        write_to_db(dht_sensor_config=sensor_config, writer=sensor_db, output_path=DEFAULT_DB)
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down sensor due to system exit | keyboard interrupt")

