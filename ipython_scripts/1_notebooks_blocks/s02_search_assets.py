# %% [markdown]
# # Getting Underway - Searching and listing registered assets
# In this notebook,
#TODO: description

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
# os.environ['USE_K8S_CLUSTER'] = 'true'
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
print("Aquarius service, base URL: {}://{}".format(res.scheme, res.netloc))
print("Aquarius service, Swagger: {}://{}/api/v1/docs/".format(res.scheme, res.netloc))
res = urllib.parse.urlparse(ocn.config['resources']['brizo.url'])
print("Brizo service, base URL: {}://{}".format(res.scheme, res.netloc))
print("Brizo service, Swagger: {}://{}/api/v1/docs/".format(res.scheme, res.netloc))
# TODO: The Swagger page does not correctly populate the /spec endpoint. Enter the URL/spec manually!


# %% [markdown]
# ### Section 2: Listing registered asset metadata in Aquarius
# All stored assets can be listed. This is typically not done in production, as the list would be too large.
# First retrieve a list of all DID's (Decentralized IDentifiers) from Aquarius.

#%%
all_dids = ocn.metadata_store.list_assets()
print("There are {} assets registered in the metadata store.".format(len(all_dids)))

# %% [markdown]
# Aquarius is a document store, with the key being the DID, and the document being the DDO
# (DID Document). The DDO describes the asset (metadata) and how to access it (Service Execution Agreement).
# For more information on these topics, please visit the Ocean Protocol standards;
#
# [OEP 7 - Decentralized Identifiers](https://github.com/oceanprotocol/OEPs/tree/master/7)
#
# [OEP 7 - Decentralized Identifiers](https://github.com/oceanprotocol/OEPs/tree/master/8
#
# Let's select the first asset for inspection (Note, since the database is stateful, this can easily change/break,
# so try with another index or register your own asset first!)
# %%
this_did = all_dids[-1]
print("Selected DID:", this_did)

# %%
# Iterating over all DID's: (can be very slow!)
# for i, did in enumerate(all_dids):
#     this_ddo= ocn.metadata_store.get_asset_metadata(did)
#     print(i, did)

# %% [markdown]
# ### Section 3: Getting a DID Documents and Assets
# %% [markdown]
# The DDO can be retrieved direct from Aquarius, as a dictionary object

#%%
# Get the DDO from Aquarius database
# TODO: This method is incorrectly named, issue opened!
aquarius_ddo = ocn.metadata_store.get_asset_metadata(this_did)

# And an asset can be created from the DDO dictionary as follows;
aquarius_asset = squid_py.ocean.asset.Asset(aquarius_ddo)
print("Asset retrieved directly from Aquarius: {}, {}".format(aquarius_asset.metadata['base']['name'], this_asset.did))

# %% [markdown]
# A DDO can be resolved from the DID on the blockchain

#%%
resolved_ddo = ocn.resolve_did(this_did)

# %% [markdown]
# However, the proper way to retrieve an asset is to **resolve** it from the Blockchain;
#%%

# TODO: This is broken!
resolved_asset = ocn.get_asset(this_did)
print(resolved_asset)
print("Resolved asset: {}, {}".format(resolved_asset.metadata['base']['name'], this_asset.did))

# %% [markdown]
# ### Section 4: Searching the Ocean
# Aquarius supports query search, the Asset class is returned

#%%
this_query = {
    "offset": 100,
    "page": 0,
    "sort": {"value": 1},
     "query": { "service":"$elemMatch":{"metadata": {$exists : true}}}}}


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
