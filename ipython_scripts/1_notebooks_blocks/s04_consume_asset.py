# %% [markdown]
# Getting Underway - Downloading Datasets (Assets)
# In this notebook, TODO: description

# %% [markdown]
# ### Section 0: Import modules, and setup logging

#%%
# Standard imports
import logging
from pprint import pprint
import os
import random
# Import mantaray and the Ocean API (squid)
import squid_py
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
import mantaray_utilities as manta_utils
from squid_py.keeper.web3_provider import Web3Provider
# Setup logging
manta_utils.logging.logger.setLevel('CRITICAL')
from mantaray_utilities.user import password_map
# manta_utils.logging.logger.setLevel('DEBUG')
# os.environ['USE_K8S_CLUSTER'] = 'True' # Enable this for testing local -> AWS setup
#%%
# Get the configuration file path for this environment
CONFIG_INI_PATH = manta_utils.config.get_config_file_path()
logging.critical("Deployment type: {}".format(manta_utils.config.get_deployment_type()))
logging.critical("Configuration file selected: {}".format(CONFIG_INI_PATH))
logging.critical("Squid API version: {}".format(squid_py.__version__))

# %% [markdown]
# ### Section 1: Instantiate a simulated User
# A 'User' in an abstract class representing a user of Ocean Protocol
#
#%%
configuration = Config(CONFIG_INI_PATH)
ocn = Ocean(configuration)
#%%
# Get a publisher account
path_passwords = manta_utils.config.get_project_path() / 'passwords.csv'
passwords = manta_utils.user.load_passwords(path_passwords)

consumer_acct = random.choice([acct for acct in ocn.accounts.list() if password_map(acct.address, passwords)])
consumer_acct.password = password_map(consumer_acct.address, passwords)
assert consumer_acct.password
print("Consumer account address: ", consumer_acct.address)
#%% [markdown]
# ### Section 2: Find an asset
#%%
#%%
# Use the Query function to get all existing assets
basic_query = {"service":{"$elemMatch":{"metadata": {"$exists" : True }}}}
all_ddos = ocn.assets.query(basic_query)
assert len(all_ddos), "There are no assets registered, go to s03_publish_and_register!"
print("There are {} assets registered in the metadata store.".format(len(all_ddos)))

assert len(all_ddos), "There are no assets registered, go to s03_publish_and_register!"

# Get a DID for testing
selected_did = all_ddos[-1].did
print("Selected DID:",selected_did)
#%% An Asset (DDO) can be also be resolved from a DID
#TODO: The Asset class does not offer much beyond DDO class
#TODO: Term 'asset' is confusing here
this_asset = ocn.assets.resolve(selected_did)
pprint(this_asset)

# %% [markdown]
# Your account will need some Ocean Token to make real transactions
# %%
# ensure Ocean token balance
if consumer_acct.ocean_balance < 50:
    tx_hash = consumer_acct.request_tokens(50)
    Web3Provider.get_web3().eth.waitForTransactionReceipt(tx_hash)

# %% [markdown]
# Purchase
# %%
# Get the service definition ID
service = this_ddo.get_service(service_type=squid_py.ServiceTypes.ASSET_ACCESS)
assert squid_py.ServiceAgreement.SERVICE_DEFINITION_ID in service.as_dictionary()
sa = squid_py.ServiceAgreement.from_service_dict(service.as_dictionary())

# This will send the purchase request to Brizo which in turn will execute the agreement on-chain
service_agreement_id = ocn.purchase_asset_service(this_ddo.did, sa.sa_definition_id, consumer_acct)
print('got new service agreement id:', service_agreement_id)


