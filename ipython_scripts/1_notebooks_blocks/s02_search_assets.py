# %% [markdown]
# # Getting Underway - Listing and searching registered assets
# In this notebook, we will explore the concept of Assets. An Asset has an ID
# (actually a 'decentralized' ID, called **DID**!).
#
# An Asset also has a document which describes the Asset and how to # authorize and gain access (i.e. purchase the asset).
# This document is called a **DDO**, the DID Document. For Data Scientists, the DDO attribute of note is the 'metadata'
# attribute. Metadata is used to describe your asset, for example the name and description of a Data Set.
#
# The DID is stored in the blockchain. The DDO is stored in a public searchable database, wrapped by the Aquarius
# component.
#
# *Note to the reader: This is a testnet: a simulated blockchain and simulated DDO store. This testnet is open to the
# public, and therefore may change state in unexpected ways (your asset might get deleted, etc.)*

# %% [markdown]
# Further reading!
#
# [W3C early draft standard 'Decentralized Identifiers (DIDs)'](https://w3c-ccg.github.io/did-spec/)
#
# [OEP 7 - Ocean Protocol standard for 'Decentralized Identifiers'](https://github.com/oceanprotocol/OEPs/tree/master/7)
#
# [OEP 7 - Ocean Protocol standard for 'Assets Metadata Ontology'](https://github.com/oceanprotocol/OEPs/tree/master/8)
#

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
import pprint

# Import mantaray and the Ocean API (squid)
import squid_py
from squid_py.ocean.ocean import Ocean
import mantaray_utilities.config as manta_config
import mantaray_utilities.logging as manta_logging
import mantaray_utilities.user as manta_user
import mantaray_utilities.asset_pretty_print as manta_print

# Setup logging
manta_logging.logger.setLevel('CRITICAL')

#%%
# Get the configuration file path for this environment
# os.environ['USE_K8S_CLUSTER'] = 'true'
CONFIG_INI_PATH = manta_config.get_config_file_path()
logging.critical("Deployment type: {}".format(manta_config.get_deployment_type()))
logging.critical("Configuration file selected: {}".format(CONFIG_INI_PATH))
logging.critical("Squid API version: {}".format(squid_py.__version__))

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
assert len(all_dids), "There are no assets registered, go to s03_publish_and_register!"
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
# ### Section 3: Low level access: getting a DID Document from Aquarius
# %% [markdown]
# The DDO can be retrieved direct from Aquarius, as a dictionary object
#
# A DDO has information regarding authentication, access control, and more
#
# For now, we will retrieve the 'metadata' of the Asset
#%%
# Get the DDO from Aquarius database
# TODO: This method is incorrectly named, issue opened and solved in last version of squid-py!
aquarius_ddo = ocn.metadata_store.get_asset_metadata(this_did)
# This is a dictionary, we are interested in only one of the 'service' items
aquarius_metadata_svc = [svc for svc in aquarius_ddo['service'] if svc['type'] == 'Metadata'][0]
aquarius_metadata = aquarius_metadata_svc['metadata']
print("Asset name:", aquarius_metadata['base']['name'])
print("Asset metadata:")
pprint.pprint(aquarius_metadata)

# %% [markdown]
# Instead of accessing the Aquarius database directly,
# a DDO can be resolved from the DID on the blockchain, which first checks if the DID exists on chain,
# and then performs the Aquarius access to return a DDO instance. A DDO instance is essentially the same as
# a dictionary object.

#%%
resolved_ddo = ocn.resolve_did(this_did)

# %% [markdown]
# The proper way to retrieve an asset is to **resolve** it from the Blockchain and return an Asset.
#%%

# TODO: This is not working in this version, update!
# resolved_asset = ocn.get_asset(this_did)
# print(resolved_asset)
# print("Resolved asset: {}, {}".format(resolved_asset.metadata['base']['name'], this_asset.did))

# %% [markdown]
# ### Section 4: Searching the Ocean
# Aquarius supports query search. A list of [Asset class] is returned from a search call.
#
# Currently, Aquarius is running MongoDB. For detailed query documentation, see the
# [documentation](https://docs.mongodb.com/manual/reference/method/db.collection.find/)
#
# TODO: Wrap queries into Utilities for higher abstraction

#%% [markdown]
# To get started, the following query will return all documents with a 'metadata' service.
#
# First, the pure mongoDB Query is built according to the documentation
#
# We are checking if the 'metadata' field exists, this should return all Assets.
#%%
basic_query = {"service":{"$elemMatch":{"metadata": {"$exists" : True }}}}
search_results = ocn.search_assets(basic_query)
print("Found {} assets".format(len(search_results)))
if search_results:
    print("First match:",search_results[0])
    manta_print.print_ddo(search_results[0].ddo)
# TODO: Update pretty-printer


#%% [markdown]
# The MongoDB search API supports pagination as well
#%%

mongo_query = {"service":{"$elemMatch":{"metadata": {"$exists" : True }}}}
full_paged_query = {"offset": 100, "page": 0, "sort": {"value": 1}, "query": mongo_query}
search_results = ocn.search_assets(full_paged_query)
print("Found {} assets".format(len(search_results)))
if search_results:
    print("First match:",search_results[0])
    manta_print.print_ddo(search_results[0].ddo)


#%% [markdown]
# Next, let's find an exact name within the 'metadata' of the Asset
#%%
match_this_name = "Ocean protocol white paper"
mongo_query = {"service":{"$elemMatch": {"metadata": {"$exists" : True }, "metadata.base.name": {'$eq':match_this_name } }}}
search_results = ocn.search_assets(mongo_query)

print("Found {} assets".format(len(search_results)))
if search_results:
    print("First match:", search_results[0])
    manta_print.print_ddo(search_results[0].ddo)

#%% Finally, let's find a substring within the name. We will use a Regex in MongoDB.
match_this_substring = 'paper'
mongo_query = {"service":{"$elemMatch": {"metadata": {"$exists" : True }, "metadata.base.name": {'$regex':match_this_substring}}}}
full_paged_query = {"offset": 100, "page": 0, "sort": {"value": 1}, "query": mongo_query}

search_results = ocn.search_assets(full_paged_query)

print("Found {} assets".format(len(search_results)))
if search_results:
    print("First match:", search_results[0])
    manta_print.print_asset(search_results[0])

# %% [markdown]
# ### Section 5: Cleaning the Ocean
# A DID is registered on the blockchain, and can be resolved to a DID Document (DDO) as presented above.
#
# Since the DDO exists on Aquarius and not in the blockchain, the DDO itself can be deleted. The DID trace can never be
# deleted from the blockchain.

#%%

if 0:
    # Let's count how many ddo's are registered
    all_dids = ocn.metadata_store.list_assets()
    print("there are {} assets registered in the metadata store.".format(len(all_dids)))

    # let's delete the first ddo object.
    first_ddo = all_dids[0]
    print("selected ddo for deletion:", first_ddo)
    ocn.metadata_store.retire_asset_metadata(first_ddo)

    # again, let's count how many ddo's are registered
    all_dids = ocn.metadata_store.list_assets()
    print("there are now {} assets registered in the metadata store.".format(len(all_dids)))

# %%
# Deleting all assets!
# Please don't delete all the assets, as other users may be testing the components!
# if 0:
#     all_dids = ocn.metadata_store.list_assets()
#     for i, did in enumerate(all_dids):
#         print("Deleting DDO {} - {}".format(i, did))
#         ocn.metadata_store.retire_asset_metadata(did)
