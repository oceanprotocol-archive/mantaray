import osmosis_aws_driver.data_S3_plugin as ocean_s3
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


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
#%% IO
# The working directory is the repo root
logging.debug("Current working directory: {}".format(os.getcwd()))
#os.path.expanduser(r"~/ocn/plankton-datascience")
#os.path.cw

#PATH_PROJECT_BASE = 
#assert os.path.exists(PATH_PROJECT_BASE)
FNAME_SOURCE_CATALOG = "Original/OceanDataSets_master catalog clean.csv"
FNAME_CURRENT_CATALOG = r"Master catalog current.csv"
PATH_SOURCE_CATALOGUE = os.path.join(os.getcwd(),'catalog', FNAME_SOURCE_CATALOG)
PATH_CURRENT_CATALOGUE = os.path.join(os.getcwd(),'catalog', FNAME_CURRENT_CATALOG)
assert os.path.exists(PATH_SOURCE_CATALOGUE), "{}".format(PATH_SOURCE_CATALOGUE)
assert os.path.exists(PATH_CURRENT_CATALOGUE), "{}".format(PATH_CURRENT_CATALOGUE)

#%% Load the data catalogue
df = pd.read_csv(PATH_CURRENT_CATALOGUE)

total_GB = sum(df.loc[:,'SizeGB'])
logging.debug("Loaded data catalogue with {} records representing {:0.0f} GB".format(len(df),total_GB))
logging.debug("{} files have been flagged as already uploaded to S3.".format(sum(df['uploaded'])))
errors = df[df['error'] != 'No error']['error'].value_counts()
logging.debug("{} files have been flagged with an upload error.".format(sum(errors)))

for err in errors.iteritems():
    print(*err)

res = df.head()
df = df[0:5]

#%% List buckets
config = dict()
config['region'] = 'eu-central-1'
ocn_s3 = ocean_s3.S3_Plugin(config)

for i,b in enumerate(ocn_s3.list_buckets()):
    print(i,b['Name'])
#%% Get the bucket
bucketname ="data-catalogue-r00"
bucket = ocn_s3.s3_client.head_bucket(Bucket=bucketname)
#%%
for row in df.iterrows():
    print(row)

#%%
df['uploaded']