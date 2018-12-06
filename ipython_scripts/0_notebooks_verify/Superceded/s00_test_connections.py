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

# The source catalog
FNAME_SOURCE_CATALOG = "Original/OceanDataSets_master catalog clean.csv"
# The current catalog stores the updated state
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

print("Error summary:")
for err in errors.iteritems():
    print('\t',*err)

res = df.head()
df = df[0:5]


#%% Create the connection via the wrapper

# The `osmosis-aws-driver`, imported here as `ocean_s3` is a wrapper for Boto3.


# config = dict()
# config['region'] = 'eu-central-1'
config = None
ocn_s3 = ocean_s3.S3_Plugin(config)

#%% List buckets

for i,b in enumerate(ocn_s3.list_buckets()):
    print(i,b['Name'])

#%% Get the bucket
bucketname ="data-catalogue-r00"
#bucket = ocn_s3.s3_client.head_bucket(Bucket=bucketname)
bucket = ocn_s3.s3_resource.Bucket(bucketname)

#%% Get the files
s3files = {obj.key:obj for obj in  bucket.objects.all()}

# Select a subset of files
these_keys = list(s3files.keys())[:2]
for f in these_keys:
    meta_data = s3files[f].Object().metadata
    print(f, meta_data)

total_GB=sum([s3files[f].size for f in s3files])/1000/1000/1000

logging.debug("{} files on {}, {:0.2f} GB".format(len(s3files),bucketname,total_GB))


#%%

#%%
for row in df.iterrows():
    print(row)

#%%
df['uploaded']

#%% Register the dataset onto blockchain