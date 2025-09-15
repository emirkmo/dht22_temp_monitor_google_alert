import logging
import logging.handlers
import sys
from main import main, DEFAULT_DB


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

try:
    # inside your script, right after you parse args:
    logging.debug(f"Using DB at: {DEFAULT_DB}", file=sys.stderr)
    main()
except (KeyboardInterrupt, SystemExit):
    print("Shutting down sensor due to system exit | keyboard interrupt")
