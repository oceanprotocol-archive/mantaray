import sys

import logging
loggers_dict = logging.Logger.manager.loggerDict

logger = logging.getLogger()
logger.handlers = []

# Set level
logger.setLevel(logging.DEBUG)

# FORMAT = "%(asctime)s - %(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"
# FORMAT = "%(asctime)s %(levelno)s: %(module)30s %(message)s"
FORMAT = "%(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"

DATE_FMT = "%Y-%m-%d %H:%M:%S"
DATE_FMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(FORMAT, DATE_FMT)

# Create handler and assign
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.handlers = [handler]
logger.debug("Logging started")

#%%
# Standard imports
import os
from pathlib import Path
import json
from time import sleep
# Ocean imports
import squid_py
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
from pprint import pprint
import mantaray_utilities as manta_utils
from mantaray_utilities.user import password_map
logging.info("squid-py Ocean API version:".format(squid_py.__version__))

#%% CONFIG

OCEAN_CONFIG_PATH = Path().cwd() / 'config_nile.ini'
assert OCEAN_CONFIG_PATH.exists(), "{} - path does not exist".format(OCEAN_CONFIG_PATH)
os.environ['OCEAN_CONFIG_PATH'] = str(OCEAN_CONFIG_PATH)

PASSWORD_PATH=Path().cwd() / ".nile_passwords"
assert PASSWORD_PATH.exists()
os.environ["PASSWORD_PATH"] = str(PASSWORD_PATH)

MARKET_PLACE_PROVIDER_ADDRESS="0x376817c638d2a04f475a73af37f7b51a2862d567"
os.environ["MARKET_PLACE_PROVIDER_ADDRESS"] = MARKET_PLACE_PROVIDER_ADDRESS

JSON_TEMPLATE = Path().cwd() / 'metadata_template.json'
assert JSON_TEMPLATE.exists()


#%%
# Get the configuration file path for this environment

logging.critical("Configuration file selected: {}".format(OCEAN_CONFIG_PATH))
# logging.critical("Deployment type: {}".format(manta_utils.config.get_deployment_type()))
logging.critical("Squid API version: {}".format(squid_py.__version__))

#%%
# Instantiate Ocean with the default configuration file.
configuration = Config(OCEAN_CONFIG_PATH)
squid_py.ConfigProvider.set_config(configuration)
ocn = Ocean(configuration)

#%%
# Get a publisher account

publisher_acct = manta_utils.user.get_account_by_index(ocn,0)

#%%
print("Publisher account address: {}".format(publisher_acct.address))
print("Publisher account Testnet 'ETH' balance: {:>6.1f}".format(ocn.accounts.balance(publisher_acct).eth/10**18))
print("Publisher account Testnet Ocean balance: {:>6.1f}".format(ocn.accounts.balance(publisher_acct).ocn/10**18))

#%%
# Get a simple example of Meta Data from the library directly
metadata = squid_py.ddo.metadata.Metadata.get_example()
print('Name of asset:', metadata['base']['name'])
# Print the entire (JSON) dictionary

with open(JSON_TEMPLATE, 'r') as f:
    metadata = json.load(f)
pprint(metadata)
# raise
#%%
print("Price of Asset:", metadata['base']['price'])
metadata['base']['price'] = "1" # Note that price is a string
print("Updated price of Asset:", metadata['base']['price'])

#%%
for i, file in enumerate(metadata['base']['files']):
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
for file_attrib in ddo.metadata['base']['files']:
    assert 'url' not in file_attrib
print("Encrypted files decrypt on purchase! Cipher text: [{}...] . ".format(ddo.metadata['base']['encryptedFiles'][:50]))

# %% [markdown]
# ## Section 4: Verify your asset
# Now, let's verify that this asset exists in the MetaData storage.
#
# A call to assets.resolve() will call the Aquarius service and retrieve the DID Document
#%% {HELLO:test}
#+attr_jupyter: some cell metadata stuff
#+attr_jupyter: some other metadata stuff

#TODO: Better handling based on reciept
print("Wait for the transaction to complete!")
sleep(10)
# %%
ddo = ocn.assets.resolve(registered_did)
print("Asset '{}' resolved from Aquarius metadata storage: {}".format(ddo.did,ddo.metadata['base']['name']))

# %% [markdown]
# Similarly, we can verify that this asset is registered into the blockchain, and that you are the owner.

# %%
# We need the pure ID string as in the DID registry (a DID without the prefixes)
asset_id = squid_py.did.did_to_id(registered_did)
owner = ocn._keeper.did_registry.contract_concise.getDIDOwner(asset_id)
print("Asset ID", asset_id, "owned by", owner)
assert str.lower(owner) == str.lower(publisher_acct.address)





#%%

import argparse
parser = argparse.ArgumentParser(description='Videos to images')
parser.add_argument('--input', type=str, help='Input dir for videos')
parser.add_argument('outtext', type=str, help='Output dir for image')

args = parser.parse_args()

print(args.audio)





