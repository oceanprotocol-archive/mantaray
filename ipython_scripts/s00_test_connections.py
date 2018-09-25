#%% Imports
import boto3

# %% Logging
import logging

loggers_dict = logging.Logger.manager.loggerDict

logger = logging.getLogger()
logger.handlers = []

# Set level
logger.setLevel(logging.DEBUG)


# FORMAT = "%(asctime)s - %(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"
FORMAT = "%(asctime)s L%(levelno)s: %(module)-15s %(message)s"

DATE_FMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(FORMAT, DATE_FMT)

# Create handler and assign
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.handlers = [handler]
logger.critical("Logging started")

#%%
print("Boto3 version:",boto3.__version__)

#%% Credentials
#TODO: Describe and link to credential management for Data Scientists

#%% A resource object is a higher level object oriented interface to the AWS API
s3_resource = boto3.resource('s3')
logging.debug("S3 resource object connected in {}".format(s3_resource))

#%% Boto3 clients (e.g. S3) expose the low level AWS service API
s3_client = boto3.client('s3')
logging.debug("S3 client object connected in {}".format(s3_client._client_config.region_name))
