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
##PATH_DATA_CATALOGUE_CLEAN = os.path.join(PATH_PROJECT_BASE,
#     'planktonDS_data_seeding/catalog/OceanDataSets_master catalog clean.csv')
#assert os.path.exists(PATH_DATA_CATALOGUE_CLEAN)

PATH_DATA_CATALOGUE_STATUS = os.path.join(PATH_PROJECT_BASE, 'planktonDS_data_seeding/catalog/Master catalog current.csv')
assert os.path.exists(PATH_DATA_CATALOGUE_STATUS)

#PATH_DATA_CATALOGUE_STATUS2 = os.path.join(PATH_PROJECT_BASE, 'planktonDS_data_seeding/catalog/OceanDataSets_master catalog clean STATUS2.csv')
#assert os.path.exists(PATH_DATA_CATALOGUE_STATUS2)

PATH_LOCAL_DATA = r"/home/batman/00 TEMP DATA"
assert os.path.exists(PATH_LOCAL_DATA)

BUCKET_NAME = "data-catalogue-r00"	
REGION = "Region EU (Frankfurt)"


#%% Load and summarize the catalogue
#df = pd.read_csv(PATH_DATA_CATALOGUE_CLEAN)
df = pd.read_csv(PATH_DATA_CATALOGUE_STATUS)

#df.to_csv(PATH_DATA_CATALOGUE_STATUS)

#df['uploaded'] =  df['hash'].isin(keys)

#mask_uploaded = df.loc[:,'hash'].isin(keys)
#sum(mask_uploaded)
#df.loc[:,'uploaded'] = mask_uploaded

#%% New columns added for status of processing
#df['error'] = ""
#df['uploaded'] = False

#PATH_DATA_CATALOGUE_STATUS = os.path.join(PATH_PROJECT_BASE,'planktonDS_data_seeding/catalog/OceanDataSets_master catalog clean STATUS.csv')
#df.to_csv(PATH_DATA_CATALOGUE_STATUS)
#df.drop('Unnamed: 0.1',axis=1,inplace=True)

#df.columns
total_GB = sum(df.loc[:,'SizeGB'])
logging.debug("Loaded data catalogue with {} records representing {:0.0f} GB".format(len(df),total_GB))
logging.debug("{} files have been flagged as already uploaded to S3.".format(sum(df['uploaded'])))

#df['error'].unique()
print("ERRORS recorded:")
for i,row in df['error'].value_counts().iteritems():
    if i:
        print("{:15} {:10}".format(i,row))

logging.debug("{} files have been flagged as causing an error".format(sum(~(df['error'] == ""))))

staged_for_upload = (df['error'] == "No error") & (~df['uploaded'])
logging.debug("{} files are staged for upload".format(sum(staged_for_upload)))


#df['error'][df['error'].isna()] = "No error"
#"None"

#df.loc[:,'SizeGB'].describe()

#df.columns
#print("Uploaded:", )
#print("Uploaded:", sum(df['error']))



#%% SUBSET OF DATA!
# Select only files less that 10MB
#df = df[df['SizeGB'] < 0.01]

sum(df['SizeGB'] > 100)

# Select top 10
#df = df[:10]

#%% Credentials
boto3.__version__

with open(PATH_CREDENTIALS, 'r') as f:
    creds = yaml.load(f)    
    
#%% Get S3 as a client
if 0:
    s3_client = boto3.client('s3', 
        aws_access_key_id=creds['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=creds['AWS_SECRET_ACCESS_KEY'],
        #region_name='eu-central-1',
        #config=botocore.client.Config(signature_version='s3v4')
        )
    
    logging.debug("S3 client: {}".format(s3_client))


#%% List buckets
if 0:
    # Call S3 to list current buckets
    # Return a the low - level HTTP response object
    response = s3_client.list_buckets()
    logging.debug("Found {} buckets".format(len(response['Buckets'])))
    
    for bucket in response['Buckets']:
        print(bucket['Name'])
        #print(bucket.name)
        

#%% Get S3 as a resource
s3 = boto3.resource('s3',
    aws_access_key_id=creds['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=creds['AWS_SECRET_ACCESS_KEY'],
    region_name='eu-central-1',
    )

logging.info("S3 resource: {}".format(s3))

#boto3.resource('iam').CurrentUser().arn.split(':')[4]

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
#url = rec['Download Link']
#target_dir = PATH_LOCAL_DATA
def download(url, target_dir):
    r = requests.get(url, stream=True)
    
    output_path = os.path.join(target_dir, 'this_file_output')
    
    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0)); 
    block_size = 1024
    wrote = 0 
    with open(output_path, 'wb') as f:
        for data in tqdm(r.iter_content(block_size), total=math.ceil(total_size//block_size) , unit='KB', unit_scale=True):
            wrote = wrote  + len(data)
            f.write(data)
    if total_size != 0 and wrote != total_size:
        print("ERROR, something went wrong")
    
    logging.debug("Downloaded {:0.1f} kB to {}".format(total_size/1000/1000,output_path))
    
    return output_path
        
#%%
meta_data_items = [
    'RecordName',
    'Download Link',
    'SizeGB',
    'Version',
    'Format',
    'License',
    'Classification',
    'UpdateFrequency',
    'LifecycleStage',
    'Description',
    'Note',
    'industry',
    'keywords',
    'Type',
    'P-ID',
    'category1',
    'category2',
    'category3',
    'category4',
    'source code License',
    'hash'
    ]

def process_meta_data(meta_data):
    
    # Ensure keys have no spaces
    meta_data = {k.replace(' ', '_'): v for k, v in meta_data.items()}
    
    # Add the current time
    meta_data['created_time'] = datetime.datetime.now().isoformat()
    
    # Ensure all strings
    meta_data = {k:str(meta_data[k]) for k in meta_data}
    
    # Additionally, MetaData must be URL encoded to be save (no slash, no colon,etc...)
    meta_data = {k:urllib.parse.quote(meta_data[k], "utf-8") for k in meta_data}
    
    # Ensure the Metadata is less than 2 KB    
    this_meta_data_size = sys.getsizeof(meta_data)
    assert this_meta_data_size < 1024 * 2
    logging.debug("{} metadata items parsed".format(len(meta_data)))
    
    return meta_data

#%% Check all metadata first!
if 0:
    for i,rec in df.iterrows():
        #logging.debug("Record {}, {} {} GB from {}".format(i,rec['RecordName'],rec['SizeGB'],rec['Download Link']))
    
        #rec['hash']
        #rec['Download Link']
        #rec['SizeGB']
        
        #--- Get and clean the metadata
        this_meta_data = process_meta_data(rec[meta_data_items].to_dict())
    

#%% Process the records

for i,rec in df[staged_for_upload].iterrows():
    logging.debug("Processing record {}, {} GB".format(i,rec['SizeGB']))

         
    #    # Skip if already uploaded
    #    if rec['uploaded'] == True: 
    #        logging.debug("{} already exists on S3".format(rec['hash']))
    #        continue
        
    # Skip if too large
    if rec['SizeGB'] > 1:
        logging.debug("{} Too large for now!".format(rec['hash']))
        continue

    
#    if not math.isnan(rec['error']):
#        type(rec['error'])
#        logging.debug("{} had an error last time".format(rec['hash']))
#        continue
    
    
    #logging.debug("Record {}, {} {} GB from {}".format(i,rec['RecordName'],rec['SizeGB'],rec['Download Link']))
    
    #--- Get and clean the metadata
    this_meta_data = process_meta_data(rec[meta_data_items].to_dict())

    
    #--- Download the file to local
    try:
        this_out_path = download(rec['Download Link'],PATH_LOCAL_DATA)
    except Exception as exception:
        df.loc[i,'error'] = type(exception).__name__
        df.to_csv(PATH_DATA_CATALOGUE_STATUS)
        continue
        #raise exception    
        
        
    #--- Upload this file with the metadata
    #print(this_meta_data)
    try:
        with open(this_out_path, 'rb') as file_obj:
            bucket.put_object(Key=rec['hash'], Metadata=this_meta_data, Body=file_obj)
    except Exception as exception:
        df.loc[i,'error'] = type(exception).__name__
        df.to_csv(PATH_DATA_CATALOGUE_STATUS)
        continue
        #raise exception    
        
    logging.info("Uploaded {} to {} with {} metadata items".format(rec['hash'],bucket,len(this_meta_data)))
    
    df.loc[i,'uploaded'] = True
    
    logging.info("{} records uploaded".format(sum(df.loc[:,'uploaded']==True)))
    
    logging.info("Saving {} to {}".format(df.shape,PATH_DATA_CATALOGUE_STATUS))
    df.to_csv(PATH_DATA_CATALOGUE_STATUS)
    
    #break