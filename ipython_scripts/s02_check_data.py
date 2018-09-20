import sys
import os
import boto3
import botocore
import time
#import datetime
import yaml
import pandas as pd
#import matplotlib
from tqdm import tqdm
import requests
import math
import datetime
import urllib

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

logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('nose').setLevel(logging.WARNING)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)


#%% IO
PATH_PROJECT_BASE = r"/home/batman/ocn/plankton-datascience"
assert os.path.exists(PATH_PROJECT_BASE)
PATH_CREDENTIALS = os.path.join(PATH_PROJECT_BASE,'keys/ocean_MyS3FullAccess.yml')
assert os.path.exists(PATH_CREDENTIALS)
PATH_DATA_CATALOGUE_CLEAN = os.path.join(PATH_PROJECT_BASE,
     'planktonDS_data_seeding/catalog/Original/OceanDataSets_master catalog clean.csv')
assert os.path.exists(PATH_DATA_CATALOGUE_CLEAN)

PATH_LOCAL_DATA = r"/home/batman/00 TEMP DATA"
assert os.path.exists(PATH_LOCAL_DATA)

BUCKET_NAME = "data-catalogue-r00"	
REGION = "Region EU (Frankfurt)"

#%% Credentials
boto3.__version__

with open(PATH_CREDENTIALS, 'r') as f:
    creds = yaml.load(f)   

#%% Get S3 as a resource
s3 = boto3.resource('s3',
    aws_access_key_id=creds['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=creds['AWS_SECRET_ACCESS_KEY'],
    region_name='eu-central-1',
    )

logging.info("S3 resource: {}".format(s3))


#%% Get target bucket
bucket = s3.Bucket(BUCKET_NAME)

try:
    s3.meta.client.head_bucket(Bucket=bucket.name)
except botocore.client.ClientError:
    print("The bucket {} does not exist in the resource".format(bucket_name))
    raise
    # The bucket does not exist or you have no access.
    
logging.debug("Bucket {}".format(bucket))

#%%
s3files = {obj.key:obj for obj in  bucket.objects.all()}

keys = s3files.keys()
for f in s3files:
    # Size in Bytes! 
    #print("File: {} Size: {}".format(f, s3files[f].size))
    pass


total_GB=sum([s3files[f].size for f in s3files])/1000/1000/1000

logging.debug("{} files on {}, {:0.2f} GB".format(len(s3files),BUCKET_NAME,total_GB))

    
#%% Get an objects' metadata
type(s3files[f])
dir(s3files[f])

dir(s3files[f].Object().metadata)
s3files[f].Object().metadata

s3files[f].meta.data


#%%

bucket.get_key(f)
