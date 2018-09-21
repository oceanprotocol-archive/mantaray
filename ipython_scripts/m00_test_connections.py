# General imports
import sys
import os
#import glob
import pandas as pd
import hashlib


#%% Logging
import logging
loggers_dict = logging.Logger.manager.loggerDict
 
logger = logging.getLogger()
logger.handlers = []

# Set level
logger.setLevel(logging.DEBUG)

# Create formatter

#FORMAT = "%(asctime)s - %(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"
FORMAT = "%(asctime)s L%(levelno)s: %(message)s"

DATE_FMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(FORMAT, DATE_FMT)

# Create handler and assign
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.handlers = [handler]
logger.critical("Logging started")



#%% IO
# The working directory is the repo root
logging.debug("Current working directory: {}".format(os.getcwd()))
#os.path.expanduser(r"~/ocn/plankton-datascience")
#os.path.cw

#PATH_PROJECT_BASE = 
#assert os.path.exists(PATH_PROJECT_BASE)
FNAME_SOURCE_CATALOG = "OceanDataSets_master catalog clean.csv"
FNAME_CURRENT_CATALOG = r"Master catalog current.csv"
PATH_SOURCE_CATALOGUE = os.path.join(os.getcwd(),'catalog', FNAME_SOURCE_CATALOG)
PATH_CURRENT_CATALOGUE = os.path.join(os.getcwd(),'catalog', FNAME_CURRENT_CATALOG)
assert os.path.exists(PATH_SOURCE_CATALOGUE), "{}".format(PATH_SOURCE_CATALOGUE)
assert os.path.exists(PATH_CURRENT_CATALOGUE), "{}".format(PATH_CURRENT_CATALOGUE)

PATH_DATA_CATALOGUE_CLEAN = os.path.join(PATH_PROJECT_BASE,'planktonDS_data_seeding/OceanDataSets_master catalog clean.csv')

#%% Load the data catalogue
df = pd.read_csv(PATH_DATA_CATALOGUE)
df.columns



#%%

import osmosis_aws_driver.data_S3_plugin as ocean_s3
dir(ocean_s3)
config = dict()
config['region'] = 'eu-central-1'
ocn_s3 = ocean_s3.S3_Plugin(config)

for i,b in enumerate(ocn_s3.list_buckets()):
    print(i,b['Name'])
#%%
    