# stdlib
import sys
import logging
from logging.handlers import RotatingFileHandler

# get logger
logger = logging.getLogger(__name__)

# create formatter
format_string = "%(asctime)s [%(levelname)s] -  %(message)s"
formatter = logging.Formatter(format_string)

# create handler
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = RotatingFileHandler(
    "./fastapi.log", maxBytes=5 * 1024 * 1024, backupCount=5
)  # 5MB per file, 5 files

# set formatter
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# set level
# Setting DEBUG level will capture all levels above it
logger.setLevel(logging.DEBUG)
# Console output shows INFO and above
stream_handler.setLevel(logging.DEBUG)
# Log file captures all levels
file_handler.setLevel(logging.DEBUG)

# add handler to logger
logger.handlers = [stream_handler, file_handler]
