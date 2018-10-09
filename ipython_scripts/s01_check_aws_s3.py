# %% [markdown]
# In this script, your connection to S3 will be checked.
#
# For configuration of credentials, see AWS documentation. Boto3 supports credential management.

# %%
## Imports
import boto3
import logging
logging.basicConfig(level=logging.DEBUG)

# %% ## Version
print("Boto3 version:",boto3.__version__)

# %% ## Credentials
#TODO: Describe and link to credential management for Data Scientists

# %% ## A resource object is a higher level object oriented interface to the AWS API
s3_resource = boto3.resource('s3')
logging.debug("S3 resource object connected in {}".format(s3_resource))

# %% ## Boto3 clients (e.g. S3) expose the low level AWS service API
s3_client = boto3.client('s3')
logging.debug("S3 client object connected in {}".format(s3_client._client_config.region_name))
