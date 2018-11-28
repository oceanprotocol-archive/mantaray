# %% Logging
import logging

loggers_dict = logging.Logger.manager.loggerDict

logger = logging.getLogger()
logger.handlers = []

# Set level
logger.setLevel(logging.DEBUG)

# FORMAT = "%(asctime)s - %(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"
# FORMAT = "%(asctime)s %(levelno)s: %(module)30s %(message)s"
FORMAT = "%(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"

DATE_FMT = "%Y-%m-%d %H:%M:%S"
DATE_FMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(FORMAT, DATE_FMT)

# Create handler and assign
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.handlers = [handler]
logger.debug("Logging started")