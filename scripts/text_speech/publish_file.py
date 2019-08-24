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
import squid_py
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
from pprint import pprint
# Setup logging
from time import sleep

logging.info("squid-py Ocean API version:".format(squid_py.__version__))

def password_map(address, password_dict):
    """Simple utility to match lowercase addresses to the password dictionary

    :param address:
    :param password_dict:
    :return:
    """
    lower_case_pw_dict = {k.lower(): v for k, v in password_dict.items()}
    if str.lower(address) in lower_case_pw_dict:
        password = lower_case_pw_dict[str.lower(address)]
        return password
    else:
        return False

#%%
# Get the configuration file path for this environment
OCEAN_CONFIG_PATH = Path(os.environ['OCEAN_CONFIG_PATH'])
assert OCEAN_CONFIG_PATH.exists(), "{} - path does not exist".format(OCEAN_CONFIG_PATH)

logging.critical("Configuration file selected: {}".format(OCEAN_CONFIG_PATH))
logging.critical("Deployment type: {}".format(manta_utils.config.get_deployment_type()))
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

publisher_acct = manta_utils.user.get_account_by_index(ocn,0)

# path_passwords = manta_utils.config.get_project_path() / 'passwords.csv'
# passwords = manta_utils.user.load_passwords(path_passwords)
#
# publisher_acct = random.choice([acct for acct in ocn.accounts.list() if password_map(acct.address, passwords)])
# publisher_acct.password = password_map(publisher_acct.address, passwords)
# assert publisher_acct.password

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
metadata = squid_py.ddo.metadata.Metadata.get_example()
print('Name of asset:', metadata['base']['name'])
# Print the entire (JSON) dictionary
pprint(metadata)

# %% [markdown]
# Note that the price is included in the Metadata! This will be purchase price you are placing on the asset. You can
# Alter the metadata object at any time before publishing.
#%%
print("Price of Asset:", metadata['base']['price'])
metadata['base']['price'] = "1" # Note that price is a string
print("Updated price of Asset:", metadata['base']['price'])

#%% [markdown]
# Let's inspect another important component of your metadata - the actual asset files. The files of an asset are
# described by valid URL's. You are responsible for ensuring the URL's are alive. Files may have additional
# information, including a checksum, length, content type, etc.

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





