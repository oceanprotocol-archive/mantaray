import shutil
from pathlib import Path
import zipfile
import logging
import random
import pandas as pd
# %%
import logging
loggers_dict = logging.Logger.manager.loggerDict
logger = logging.getLogger()
logger.handlers = []
# Set level
logger.setLevel(logging.DEBUG)
FORMAT = "%(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(FORMAT, DATE_FMT)
# Create handler and assign
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.handlers = [handler]
logger.info("Logging started")

# %%
path_data_root = Path.home() / 'DATA'

data_paths = [p for p in path_data_root.iterdir() if p.is_dir()]

for ds in data_paths:
    logging.debug("Processing {} dataset".format(ds))
    path_metadata = ds / 'metadata.json'
    if path_metadata.exists():
        logging.debug(f"Metadata loaded".format())
