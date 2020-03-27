# %% [markdown]
# # Getting Underway - Publishing assets
# In this notebook, we will explore how to publish an Asset using Ocean Protocol.
# As described in the previous notebook, Publish consists of 2 aspects:
#
# 1. Uploading the DDO to Aquarius
# 1. Registering the Asset on the blockchain

# %% [markdown]
# ### Section 0: Import modules, and setup logging

#%%
# Standard imports
import json
import logging

# Import mantaray and the Ocean API (squid)
import squid_py
from mantaray_utilities.mantaray_utilities.user import create_account
from ocean_utils.agreements.service_factory import ServiceDescriptor
from ocean_utils.agreements.service_types import ServiceTypes
from ocean_utils.did import did_to_id
from squid_py.brizo import BrizoProvider
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
from mantaray_utilities import logging as manta_logging, config, asset_pretty_print
from mantaray_utilities.misc import get_metadata_example

from pprint import pprint

# Setup logging
manta_logging.logger.setLevel('CRITICAL')

#%%
# Get the configuration file path for this environment
# os.environ['USE_K8S_CLUSTER'] = 'true'
CONFIG_INI_PATH = config.get_config_file_path()
logging.critical("Deployment type: {}".format(config.get_deployment_type()))
logging.critical("Configuration file selected: {}".format(CONFIG_INI_PATH))
logging.critical("Squid API version: {}".format(squid_py.__version__))

# %% [markdown]
# ### Section 1: Instantiate a simulated User
# A 'User' in an abstract class representing a user of Ocean Protocol.
#

# Instantiate Ocean with the default configuration file.
configuration = Config(CONFIG_INI_PATH)
ocn = Ocean(configuration)
faucet_url = ocn.config.get('keeper-contracts', 'faucet.url')

# Get the publisher account
publisher_acct = create_account(faucet_url, wait=True)

# %% [markdown]
# Your account will need some Ocean Token to make real transactions
# %%
# ensure Ocean token balance
if ocn.accounts.balance(publisher_acct).ocn == 0:
    ocn.accounts.request_tokens(publisher_acct, 10)

#%% [markdown]
# ### Section 2: Create your MetaData for your asset
# A more complex use case is to manually generate your metadata conforming to Ocean standard, but for demonstration purposes,
# a utility in squid-py is used to generate a sample Meta Data dictionary.

#%%
# Get a simple example of Meta Data from the library directly
metadata = get_metadata_example()

print('Name of asset:', metadata['main']['name'])
pprint(metadata)

asset_price = 10  # Ocean Token
service_timeout = 600  # 10 Minutes

# %% [markdown]
# When publishing a dataset, you are actually publishing *access* to the dataset. Access is negotiated by the access agent, called 'Brizo'.
# %%
brizo = BrizoProvider.get_brizo()
service_url = brizo.get_consume_endpoint(configuration)
print("To download the dataset, a user will call", service_url)

# %% [markdown]
# These purchase and download functions are packaged into a *Service Descriptor*.
# In the general case, a dataset is just a type of Asset. An Asset can be any digital asset on Ocean Protocol, including things like
# Compute services, which can have complex access methods, hence the flexibility and composability of Service Descriptors.
# The following cell displays the access service descriptor. As a publisher, you will set the price in the Meta Data
# %%
template_ID = ocn.keeper.template_manager.create_template_id(
  ocn.keeper.template_manager.SERVICE_TO_TEMPLATE_NAME[ServiceTypes.ASSET_ACCESS]
)
attributes = {
    'main': {
        "name": "dataAssetAccessServiceAgreement",
        "creator": "",
        "datePublished": "2019-02-08T08:13:49Z",
        "price": str(asset_price),
        "timeout": service_timeout
    }
}
dataset_access_service = ServiceDescriptor.access_service_descriptor(
    attributes, service_url, template_ID
)
service_descriptors = [dataset_access_service]
pprint(service_descriptors)

# %% [markdown]
# The asset has been constructed, we are ready to publish to Ocean Protocol!
# %%
ddo = ocn.assets.create(metadata, publisher_acct)

#%%
# Inspect the new DDO
# Your assigned DID:
registered_did = ddo.did
print("New asset registered at", registered_did)
asset_pretty_print.print_ddo(ddo)

# %% [markdown]
# Verify that this asset exists in the MetaData storage
# %%
ddo = ocn.assets.resolve(registered_did)

# %% [markdown]
# And this is what you would expect if the DID is *NOT* in the database
# %%
random_did = 'did:op:9a3c2693c1f942b8a61cba7d212e5cd50c1b9a5299f74e39848e9b4c2148d453'
try:
    ocn.assets.resolve(random_did)
except Exception as e:
    print("This raises an error, as required:", e)

# %% [markdown]
# Similarly, we can verify that this asset is registered into the blockchain, and that you are the owner
# %%
# We need the pure ID string (a DID without the prefixes)
asset_id = did_to_id(registered_did)
owner = ocn.keeper.did_registry.get_did_owner(asset_id)
print("Asset ID", asset_id, "owned by", owner)
assert str.lower(owner) == str.lower(publisher_acct.address)
