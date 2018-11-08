import shutil
from pathlib import Path
import zipfile
import logging
import random
import pandas as pd
import json
import pandas as pd
import requests

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
            print(res.status_code,link)
            res = requests.head(url)
            # print(res.status_code)
            assert res.status_code == 200
            # logging.debug(f"{link}".format())
# %%
# Check all the content URLs
for name in metadata_dict:
    meta = metadata_dict[name]
    for link in meta['base']['contentUrls']:
        res = requests.head(link)
        print(res.status_code,link)
        assert res.status_code == 200
            # logging.debug(f"{link}".format())


#         res = requests.get(link)
# requests.post('https://s3.eu-central-1.amazonaws.com/trilobite/World_Population/full/WPP2017_POP_F01_1_TOTAL_POPULATION_BOTH_SEXES.xlsx')
# requests.get('https://s3.eu-central-1.amazonaws.com/trilobite/World_Population/full/WPP2017_POP_TOTAL_POPULATION_BOTH_SEXES.xlsx')
# requests.head('https://s3.eu-central-1.amazonaws.com/trilobite/World_Population/full/WPP2017_POP_F01_1_TOTAL_POPULATION_BOTH_SEXES.xlsx')
