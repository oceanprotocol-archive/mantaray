# %% [markdown]
# Getting Underway - Downloading Datasets (Assets)
# In this notebook, TODO: description

# %% [markdown]
# ### Section 0: Import modules, and setup logging

#%%
# Standard imports
import logging

# Import mantaray and the Ocean API (squid)
import squid_py
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
import mantaray_utilities as manta_utils
# Setup logging
manta_utils.logging.logger.setLevel('CRITICAL')
# manta_utils.logging.logger.setLevel('DEBUG')

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
# Get the consumer account
consumer_address = configuration['keeper-contracts']['parity.address']
consumer_pass = configuration['keeper-contracts']['parity.password']
consumer_acct = [ocn.accounts[addr] for addr in ocn.accounts if addr.lower() == consumer_address.lower()][0]
consumer_acct.password = consumer_pass
print("Consumer account address: ", consumer_acct.address)
#%% [markdown]
# ### Section 2: Find an asset
#%%
# Get ALL dids
all_dids = ocn.metadata_store.list_assets()
print("There are {} assets registered in the metadata store.".format(len(all_dids)))

assert len(all_dids), "There are no assets registered, go to s03_publish_and_register!"

# Get a DID for testing
selected_did = all_dids[-1]
print("Selected DID:",selected_did)
# selected_did = "did:op:d67397a67ced44bb93df65021c8b92ee7bf62b6fe4b24378b37349a290f6113c"
#%% From this DID, get the DDO
this_ddo = ocn.resolve_asset_did(selected_did)
# manta_utils.logging.logger.setLevel('CRITICAL')
# manta_utils.logging.logger.setLevel('DEBUG')

service = this_ddo.get_service(service_type=squid_py.ServiceTypes.ASSET_ACCESS)
assert squid_py.ServiceAgreement.SERVICE_DEFINITION_ID in service.as_dictionary()
sa = squid_py.ServiceAgreement.from_service_dict(service.as_dictionary())

# This will send the purchase request to Brizo which in turn will execute the agreement on-chain
service_agreement_id = ocn.purchase_asset_service(this_ddo.did, sa.sa_definition_id, consumer_acct)
print('got new service agreement id:', service_agreement_id)

# manta_utils.logging.logger.setLevel('CRITICAL')
# manta_utils.logging.logger.setLevel('DEBUG')

#%% [markdown]
# ### Section 3: Execute the agreement (purchase!)
#%%
# This will send the purchase request to Brizo which in turn will execute the agreement on-chain
# this_did = 'did:op:0x23d76f6f5e1040c8bba8701fdaa59e28bf2c9edd3acc400aa8af46fe1433344e'
# this_did = this_ddo.did
# service_agreement_id = consumer.ocn.sign_service_agreement(this_did, sa.sa_definition_id, consumer_address)
# print('got new service agreement id:', service_agreement_id)

#%% [markdown]
# Upon successful execution of the service agreement, a download is immediately initiated.
# The downloaded files are stored in the current directory in a /downloads/datafile.<did> folder.
# Check the directory in the JupyterLab notebook pane on the left, and find your Assetgi!

