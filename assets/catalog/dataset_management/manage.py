import shutil
from pathlib import Path
import zipfile
import logging
import random
import pandas as pd
import json
import pandas as pd
import requests
from pprint import pprint
from urllib.parse import urlparse

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

class LoggerCritical:
    def __enter__(self):
        my_logger = logging.getLogger()
        my_logger.setLevel("CRITICAL")
    def __exit__(self, type, value, traceback):
        my_logger = logging.getLogger()
        my_logger.setLevel("DEBUG")

# %%
path_data_root = Path.home() / 'DATA'

data_paths = [p for p in path_data_root.iterdir() if p.is_dir()]

metadata_dict = dict()
for ds in data_paths:
    logging.debug("Processing {} dataset".format(ds))
    metadata_file = ds / 'metadata.json'
    if metadata_file.exists():
        with metadata_file.open() as f:
            meta = json.load(f)
            #TODO: Assert valid structure!
        metadata_dict[meta['base']['name']] = meta
        logging.debug(f"Metadata loaded for {meta['base']['name']}".format())
# pprint(metadata_dict)

#%%
# Build a summary table
df_rows = list()
for name in metadata_dict:
    meta = metadata_dict[name]
    sample = False
    discoverImage = False
    if 'links' in meta['base']:
        for link in meta['base']['links']:
            if link['type'] == 'sample':
                sample = True
            if link['type'] == 'discoverImage':
                discoverImage = True

    this_row = {
        'name' : meta['base']['name'],
        'size' : meta['base']['size'],
        'downloads' : len(meta['base']['contentUrls']),
        'sample' : sample,
        'discoverImage' : discoverImage,
    }
    df_rows.append(this_row)
df = pd.DataFrame(df_rows)

# %%
# Check all the links
for name in metadata_dict:
    meta = metadata_dict[name]
    if 'links' in meta['base']:
        for link in meta['base']['links']:
            url = link['url']
            with LoggerCritical():
                res = requests.head(url)
            fname = urlparse(url).path.split('/')[-1]
            print(res.status_code,fname)
            assert res.status_code == 200




# %%
# Check all the content URLs
for name in metadata_dict:
    meta = metadata_dict[name]
    for link in meta['base']['contentUrls']:
        with LoggerCritical():
            res = requests.head(link)
        fname = urlparse(link).path.split('/')[-1]
        print(res.status_code,fname )
        assert res.status_code == 200
