import logging
from logging.handlers import RotatingFileHandler
import os
from utils.config import get_config

config = get_config()
log_file = config["logging"]["file_path"]

os.makedirs(os.path.dirname(log_file), exist_ok=True)

app_logger = logging.getLogger("invoice_logger")
app_logger.setLevel(getattr(logging, config["logging"]["log_level"], "INFO"))

formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")

file_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

if not app_logger.hasHandlers():
    app_logger.addHandler(file_handler)
    app_logger.addHandler(stream_handler)