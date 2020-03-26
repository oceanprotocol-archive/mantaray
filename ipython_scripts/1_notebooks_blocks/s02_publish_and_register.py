# %% [markdown]
# # Getting Underway - Publishing assets
# In this notebook, we will explore how to publish an Asset using Ocean Protocol. An Asset consists of several files
# which are kept private, and optionally other links which are open (samples, descriptions, etc.).
#
# A publisher will require access to two services;
# 1. A service to store the MetaData of the asset (part of the DDO) - 'Aquarius'
# 1. A service to manage permissioned access to the assets - 'Brizo'
#
# The publishing of an asset consists of;
# 1. Preparing the asset files locally
# 1. Preparing the metadata of the asset
# 1. Uploading assets or otherwise making them available as URL's
# 1. Registering the metadata and service endpoints into Aquarius
# 1. Registering the asset into the Blockchain (into the DID Registry)

# %% [markdown]
# <p><img src="https://raw.githubusercontent.com/oceanprotocol/mantaray/develop/doc/img/jupyter_cell.png" alt="drawing" width="400" align="center"/></p>
# <p><b>Overall client and service architecture</b></p>

# %% [markdown]
# ### Section 0: Import modules, connect the Ocean Protocol API

#%%
# Standard imports
import json
import logging
import os
from pathlib import Path
from time import sleep

# Import mantaray and the Ocean API (squid)
import random
import squid_py
from ocean_keeper.utils import get_account
from ocean_keeper.web3_provider import Web3Provider
from ocean_utils.did import did_to_id
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
from mantaray_utilities import logging as manta_logging, config
from mantaray_utilities.misc import get_metadata_example

from pprint import pprint

# Setup logging
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
# ### Section 1: A publisher account in Ocean

#%%
# Get a publisher account

publisher_acct = get_account(0)

#%%
print("Publisher account address: {}".format(publisher_acct.address))
print("Publisher account Testnet 'ETH' balance: {:>6.1f}".format(ocn.accounts.balance(publisher_acct).eth/10**18))
print("Publisher account Testnet Ocean balance: {:>6.1f}".format(ocn.accounts.balance(publisher_acct).ocn/10**18))

# %% [markdown]
# Your account will need some Ocean Token to make real transactions, let's ensure that you are funded!

# %%
# ensure Ocean token balance
# if ocn.accounts.balance(publisher_acct).ocn == 0:
#     ocn.accounts.request_tokens(publisher_acct, 100)

#%% [markdown]
# ### Section 2: Create the Metadata for your asset
# The metadata is a key-value set of attributes which describe your asset
#
# A more complex use case is to manually generate your metadata conforming to Ocean standard, but for demonstration purposes,
# a utility in squid-py is used to generate a sample Meta Data dictionary.

#%%
# Get a simple example of Meta Data from the library directly
metadata = get_metadata_example()

print('Name of asset:', metadata['main']['name'])
# Print the entire (JSON) dictionary
pprint(metadata)

# %% [markdown]
# Note that the price is included in the Metadata! This will be purchase price you are placing on the asset. You can
# Alter the metadata object at any time before publishing.
#%%
print("Price of Asset:", metadata['main']['price'])
metadata['main']['price'] = "9"  # Note that price is a string
print("Updated price of Asset:", metadata['main']['price'])

#%% [markdown]
# Let's inspect another important component of your metadata - the actual asset files. The files of an asset are
# described by valid URL's. You are responsible for ensuring the URL's are alive. Files may have additional
# information, including a checksum, length, content type, etc.

#%%
for i, file in enumerate(metadata['main']['files']):
    print("Asset link {}: {}".format( i, file['url']))

# %% [markdown]
# ## Section 3 Publish the asset
# With this metadata object prepared, we are ready to publish the asset into Ocean Protocol.
#
# The result will be an ID string (DID) registered into the smart contract, and a DID Document stored in Aquarius.
# The asset URLS's are encrypted upon publishing.

# %%
ddo = ocn.assets.create(metadata, publisher_acct)
registered_did = ddo.did
print("New asset registered at", registered_did)
# %% [markdown]
# Inspect the new DDO. We can retrieve the DDO as a dictionary object, feel free to explore the DDO in the cell below!
#%%
ddo_dict = ddo.as_dictionary()
print("DID:", ddo.did)
print("Services within this DDO:")
for svc in ddo_dict['service']:
    print(svc['type'], svc['serviceEndpoint'])

# %% [markdown]
# Note that the 'files' attribute has been modified - all URL's are now removed, and a new 'encryptedFiles'
# attribute is created to store the actual URLs.
#%%
for file_attrib in ddo.metadata['main']['files']:
    assert 'url' not in file_attrib
print("Encrypted files decrypt on purchase! Cipher text: [{}...] . ".format(ddo.metadata['encryptedFiles'][:50]))

# %% [markdown]
# ## Section 4: Verify your asset
# Now, let's verify that this asset exists in the MetaData storage.
#
# A call to assets.resolve() will call the Aquarius service and retrieve the DID Document
#%% {HELLO:test}
#+attr_jupyter: some cell metadata stuff
#+attr_jupyter: some other metadata stuff

# TODO: Better handling based on reciept
print("Wait for the transaction to complete!")
sleep(10)
web3 = Web3Provider.get_web3()
event = ocn.keeper.did_registry.subscribe_to_event(
    ocn.keeper.did_registry.DID_REGISTRY_EVENT_NAME,
    30,
    {'_did': web3.toBytes(hexstr=ddo.asset_id)},
    from_block=0,
    wait=True
)

# %%
ddo = ocn.assets.resolve(registered_did)
print("Asset '{}' resolved from Aquarius metadata storage: {}".format(ddo.did, ddo.metadata['main']['name']))

# %% [markdown]
# Similarly, we can verify that this asset is registered into the blockchain, and that you are the owner.

# %%
# We need the pure ID string as in the DID registry (a DID without the prefixes)
asset_id = did_to_id(registered_did)
owner = ocn.keeper.did_registry.contract_concise.getDIDOwner(asset_id)
print("Asset ID", asset_id, "owned by", owner)
assert str.lower(owner) == str.lower(publisher_acct.address)

# %% [markdown]
# Congratulations on publishing an Asset into Ocean Protocol!
#
# Next, let's search for our assets in Ocean Protocol


