# %% [markdown]
#

# %%
## Imports
import boto3
import logging
logging.basicConfig(level=logging.DEBUG)

# %% ## Version
print("Boto3 version:",boto3.__version__)

# %%
# ## Credentials
# 1. The order in which boto3 searches for credentials;
# 1. Passing credentials as parameters in the boto.client() method
# 1. Passing credentials as parameters when creating a Session object
# 1. Environment variables
# 1. Shared credential file (~/.aws/credentials)
# 1. AWS config file (~/.aws/config)
# 1. Assume Role provider
# 1. Boto2 config file (/etc/boto.cfg and ~/.boto)
# 1. Instance metadata service on an Amazon EC2 instance that has an IAM role configured.

#TODO: Describe and link to credential management for Data Scientists

# %%
# A session stores configuration state and allows you to create service clients and resources
# The credentials are defined in the ~/.aws folder
# Seperate profiles can be defined and selected
boto_sess = boto3.Session(profile_name='kubernetes')

# %%
# List the available clients
boto_sess.get_available_services()

# %%
# Get an IAM client
client_iam = boto_sess.client('iam')
# %%
roles = client_iam.list_roles()
Role_list = roles['Roles']
for key in Role_list:
    print(key['RoleName'])
    print(key['Arn'])

# %%
# ## Boto3 clients (e.g. S3) expose the low level AWS service API
s3_client = boto3.client('s3')
# %%
logging.debug("S3 client object connected in {}".format(s3_client._client_config.region_name))
