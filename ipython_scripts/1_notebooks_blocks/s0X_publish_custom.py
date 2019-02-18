#%%
# Standard imports
import logging

# Import mantaray and the Ocean API (squid)
import random
import squid_py
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
import mantaray_utilities as manta_utils
from mantaray_utilities.user import password_map
from pprint import pprint
import requests
# Setup logging
manta_utils.logging.logger.setLevel('CRITICAL')
manta_utils.logging.logger.setLevel('DEBUG')
from time import sleep
#%%
# Get the configuration file path for this environment
CONFIG_INI_PATH = manta_utils.config.get_config_file_path()
logging.critical("Deployment type: {}".format(manta_utils.config.get_deployment_type()))
logging.critical("Configuration file selected: {}".format(CONFIG_INI_PATH))
logging.critical("Squid API version: {}".format(squid_py.__version__))

#%%
# Instantiate Ocean with the default configuration file.
configuration = Config(CONFIG_INI_PATH)
ocn = Ocean(configuration)

# %% [markdown]
# ### Section 1: A publisher account in Ocean

#%%
# Get a publisher account
path_passwords = manta_utils.config.get_project_path() / 'passwords.csv'
passwords = manta_utils.user.load_passwords(path_passwords)

publisher_acct = random.choice([acct for acct in ocn.accounts.list() if password_map(acct.address, passwords)])
publisher_acct.password = password_map(publisher_acct.address, passwords)
assert publisher_acct.password

#%%
print("Publisher account address: {}".format(publisher_acct.address))
print("Publisher account balance:", ocn.accounts.balance(publisher_acct).ocn)

# %% [markdown]
# Your account will need some Ocean Token to make real transactions, let's ensure that you are funded!

# %%
# ensure Ocean token balance
if ocn.accounts.balance(publisher_acct).ocn == 0:
    ocn.accounts.request_tokens(publisher_acct, 100)


#%% [markdown]
# %%

this_url = "https://s3.amazonaws.com/datacommons-seeding-us-east/10_Monkey_Species_Small/remote_metadata_clean.json"
response = requests.get(this_url)
if response.status_code == 200:
    metadata = response.json()
else:
    raise
# pprint(metadata)

print("Name of Asset:", metadata['base']['name'])
print("Price of Asset:", metadata['base']['price'])

#%%
for i, file in enumerate(metadata['base']['files']):
    print("Asset link {}: {}".format( i, file['url']))

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
# Note that the 'files' attribute has been replaced by the 'encryptedFiles' attribute!
#%%
assert 'files' not in ddo.metadata['base']
print("Encryped 'files' attribute, everything safe and secure!")
print("Encrypted files decrypt on purchase! [{}...] etc. ".format(ddo.metadata['base']['encryptedFiles'][:50]))

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
# For illustrative purposes, this is the error you can expect if the DID is *NOT* in the database
# %%
random_did = 'did:op:9a3c2693c1f942b8a61cba7d212e5cd50c1b9a5299f74e39848e9b4c2148d453'
try: ocn.assets.resolve(random_did)
except Exception as e: print("(This raises, as required)", e)

# %% [markdown]
# Similarly, we can verify that this asset is registered into the blockchain, and that you are the owner.
#
# Congratulations on publishing an Asset into Ocean Protocol!

# %%
# We need the pure ID string as in the DID registry (a DID without the prefixes)
asset_id = squid_py.did.did_to_id(registered_did)
owner = ocn._keeper.did_registry.contract_concise.getOwner(asset_id)
print("Asset ID", asset_id, "owned by", owner)
assert str.lower(owner) == str.lower(publisher_acct.address)

# %% [markdown]
# Next, let's search for our assets in Ocean Protocol


