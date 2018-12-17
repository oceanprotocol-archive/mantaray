# %% [markdown]
# # Getting Underway - Searching and listing registered assets
# In this notebook,
#TODO: description
#TODO: This script needs to be updated for Alpha!

# %% [markdown]
# ### Section 0: Import modules, and setup logging

#%%
# Standard imports
import sys
import logging
from pathlib import Path
import squid_py
from squid_py.ocean.ocean import Ocean
import requests
import json
import os
import urllib

# Import mantaray and the Ocean API (squid)
import squid_py
from squid_py.ocean.ocean import Ocean
import mantaray_utilities.config as manta_config
import mantaray_utilities.logging as manta_logging
import mantaray_utilities.user as manta_user
import mantaray_utilities.asset_pretty_print as manta_print

# Setup logging
manta_logging.logger.setLevel('INFO')

#%%
# Get the configuration file path for this environment
os.environ['USE_K8S_CLUSTER'] = 'true'
CONFIG_INI_PATH = manta_config.get_config_file_path()
logging.info("Deployment type: {}".format(manta_config.get_deployment_type()))
logging.info("Configuration file selected: {}".format(CONFIG_INI_PATH))
logging.info("Squid API version: {}".format(squid_py.__version__))

# %% [markdown]
# ### Section 1: Assets in the MetaData store (Aquarius)
# Anyone can search assets in the public metadata stores
#%%

ocn = Ocean(config_file=CONFIG_INI_PATH)

#%% [markdown]
# The Metadata store is a database wrapped with a REST API
# For all the functionality, see the Swagger documentation
#%%
res = urllib.parse.urlparse(ocn.metadata_store._base_url)
print("Aquarius service, REST API base URL: {}://{}".format(res.scheme, res.netloc))
print("Aquarius service, Swagger: {}://{}/api/v1/docs/".format(res.scheme, res.netloc))
res = urllib.parse.urlparse(ocn.config.brizo_url)
# TODO: The Swagger page does not correctly populate the /spec endpoint. Enter manually the URL/spec!

#%% [markdown]
# Brizo is an interface for asset access control.
#%%
# TODO: Brizo is not part of squid,
# print("Brizo service, REST API base URL: {}://{}".format(res.scheme, res.netloc))
# print("Brizo service, Swagger: {}://{}/api/v1/docs/".format(res.scheme, res.netloc))
# http://ac8b5e618ef0511e88a360a98afc4587-575519081.us-east-1.elb.amazonaws.com:5000/spec
# %% [markdown]
# All stored assets can be listed. This is typically not done in production, as the list would be too large.
# For demonstration purposes, we can access the REST API directly, first retrieve their DID string;
#%%
all_dids = ocn.metadata_store.list_assets()
print("There are {} assets registered in the metadata store.".format(len(all_dids)))

for i, did in enumerate(all_dids):
    this_metadata = ocn.metadata_store.get_asset_metadata(did)
    print(i, did)

# first_did = all_dids[0]
# first_id = first_did.split(':')[-1]
# first_id_int = int(first_id,16)
# %% [markdown]
# Then, the assets can be retrieved;
#%%
# TODO: Fix!
ocn.get_asset(first_did)
this_asset_endpoint = ocn.metadata_store._base_url  + '/' + first_did
result = requests.get(this_asset_endpoint).content

# %% [markdown]
# These assets can also be searched, the Asset class is returned from a search
#%% A full text search is implemented
sample_meta_data = squid_py.ddo.metadata.Metadata.get_example()

ocn.search_assets('Random Text')
ocn.search_assets('')
ocn.search_assets('asdfasdfasdf')
res = ocn.search_assets('Hello do not give me csv')
this = res[0]
this.asset_id
this.did
ocn.search_assets('Ocean')
ocn.search_assets('id')
ocn.search_assets('compression')
ocn.search_assets('contenttype = csv')


for asset in ocn.search_assets('Ocean'):
    print("\nASSET FOUND:", asset)
    print('Asset:')
    util_pprint.print_asset(asset)
    print('DDO:')
    util_pprint.print_ddo(asset.ddo)


# %% [markdown]
# Finally, assets can be deleted from the store
result = requests.get(ocn.metadata_store._base_url).content
all_dids = json.loads(result)['ids']
for i, did in enumerate(all_dids):
    print("Deleting", did)
    ocn.metadata_store.retire_asset_metadata(did)
