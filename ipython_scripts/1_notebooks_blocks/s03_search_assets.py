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
import logging
import os
from pathlib import Path

# Import mantaray and the Ocean API (squid)
import squid_py
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config

# Setup logging
from util import logging as manta_logging, config

manta_logging.logger.setLevel('INFO')
print("squid-py Ocean API version:", squid_py.__version__)
#%%
# Get the configuration file path for this environment
OCEAN_CONFIG_PATH = Path(os.path.expanduser(os.environ['OCEAN_CONFIG_PATH']))
assert OCEAN_CONFIG_PATH.exists(), "{} - path does not exist".format(OCEAN_CONFIG_PATH)

logging.critical("Configuration file selected: {}".format(OCEAN_CONFIG_PATH))
logging.critical("Deployment type: {}".format(config.get_deployment_type()))
logging.critical("Squid API version: {}".format(squid_py.__version__))

#%%
# Instantiate Ocean with the default configuration file.
configuration = Config(OCEAN_CONFIG_PATH)
squid_py.ConfigProvider.set_config(configuration)
ocn = Ocean(configuration)

# %% [markdown]
# ### Section 1: Assets are stored in the Metadata store (Aquarius) as a DDO
# Anyone can search assets in the public metadata stores. Anyone can start their own metadata instance for thier
# own marketplace.

#%% [markdown]
# The Metadata store is a database wrapped with a REST API.
# The database is accessed with a driver, currently Mongo DB is implemented.
# For more details of functionality, see the documentation and our Swagger API page.
#
# (Aquarius metadata store)[https://github.com/oceanprotocol/aquarius/tree/develop/aquarius]
#
# (MongoDB driver)[https://github.com/oceanprotocol/oceandb-mongodb-driver]

# %% [markdown]
# ### Section 2: Test search
#%%
# %% [markdown]
# ### Section 2: Listing registered asset metadata in Aquarius
# First, we will retrieve a list of DID's (Decentralized IDentifiers) from Aquarius matching any string.
# The query is limited to 100 results by default, this limit can be increased.
#%%
# Use the Query function to get all existing assets
all_ddos = ocn.assets.query({"text":['']},)
assert len(all_ddos), "There are no assets registered, go to s03_publish_and_register!"
print("Found the first {} assets registered in the metadata store.".format(len(all_ddos)))

# %% [markdown]
# Aquarius is a document store, with the key being the DID, and the document being the DDO
# (DID Document). The DDO describes the asset (metadata) and how to access it (Service Execution Agreement).
# For more information on these topics, please visit the Ocean Protocol standards;
#
# [OEP 7 - Decentralized Identifiers](https://github.com/oceanprotocol/OEPs/tree/master/7)
#
# [OEP 7 - Decentralized Identifiers](https://github.com/oceanprotocol/OEPs/tree/master/8)
#
# Let's select an asset DDO for inspection (Note, since the database is stateful, this can easily change/break,
# so try with another index or register your own asset first!)
# %%
# Select a single asset DDO from the list
this_ddo = all_ddos[-1]
print("Selected asset DID: {}".format(this_ddo.did))
print("Asset name:", this_ddo.metadata['main']['name'])
print("Asset price: {} token".format(this_ddo.metadata['main']['price']))
print("Asset description: {} token".format(this_ddo.metadata['additionalInformation']['description']))

# %% [markdown]
# ### Section 3: Searching the Ocean
# Aquarius supports query search. A list of [DDO] is returned from a search call.
#
# Currently, Aquarius is running MongoDB. For detailed query documentation, see the
# [documentation](https://docs.mongodb.com/manual/reference/method/db.collection.find/)
#
# The exposed query endpoint is a subset of the full MongoDB search capability. For the documentation on the
# Current search implementation, see https://github.com/oceanprotocol/aquarius/blob/develop/docs/for_api_users/API.md

#%% [markdown]
# #### Filter on price
# To get started, the following query will return all documents with a 'price' between 0 and 20.
# The syntax for this query, is a range of integers for the registered price.
#%%
price_filter = [5,20]
query = {"query":{"price":price_filter}}
search_results = ocn.assets.query(query)
print("Found {} assets matching price interval {}".format(len(search_results), price_filter))
all_prices = [result.metadata['main']['price'] for result in search_results]
if all_prices:
    print("Average price in this set: {:0.2f}".format(sum(all_prices)/len(all_prices)))

#%% [markdown]
# #### Text search
# Plain text search is supported, searching in all assets
#%%
query = {"query":{"text":["Weather"]}}
search_results = ocn.assets.query(query)
print("Found {} assets".format(len(search_results)))

all_names = [result.metadata['main']['name'] for result in search_results]
from collections import Counter
for name, count in dict(Counter(all_names)).items():
    print("Found {} of '{}'".format(count, name))

#%% [markdown]
# #### Combined search
# Multiple queries can be joined to create more complex filters
#%%
query = {"query":{"text":["Weather"],"price":[0,11]}}
search_results = ocn.assets.query(query)
print("Found {} assets".format(len(search_results)))
print_match_idx = -1
for result in search_results:
    print("Selected asset: {}, price:{}, {}".format(result.metadata['main']['name'],result.metadata['main']['price'], result.did ))
