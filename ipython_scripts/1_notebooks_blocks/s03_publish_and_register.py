# %% [markdown]
# # Getting Underway - Publishing assets
# In this notebook, we will explore how to publish an Asset using Ocean Protocol.
# As described in the previous notebook, Publish consists of 2 aspects:
#
# 1. Uploading the DDO to Aquarius
# 1. Registering the Asset on the blockchain
#
# *Note to the reader! The current implementation is very low-level, most of the functionality will be wrapped into
# simpler Ocean.publish_dataset() style methods!*
# %% [markdown]
# ### Section 0: Import modules, and setup logging

#%%
# Standard imports
import logging
from pathlib import Path
import os

# Import mantaray and the Ocean API (squid)
import squid_py
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
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
# ### Section 1: Instantiate a simulated User
# A 'User' in an abstract class representing a user of Ocean Protocol.
#
#%%
# Instantiate Ocean with the default configuration file.
configuration = Config(CONFIG_INI_PATH)
ocn = Ocean(configuration)

#%% [markdown]
# For this tutorial, we will select one of the available unlocked accounts.
#
# In general, as a publisher, you will have your own configuration file with your personal account.

#%%
# This utility function gets all simulated accounts.
# Let's take the first unlocked account, and name it the Publisher.
publisher = manta_user.get_first_user(ocn.accounts)
print(publisher)

assert publisher.ocn._http_client.__name__ == 'requests'
assert publisher.ocn._secret_store_client.__name__ == 'Client'

# We don't need this ocn instance reference anymore ...
del ocn
#%% [markdown]
# ### Section 2: Create your MetaData for your asset
# A more complex use case is to manually generate your metadata conforming to Ocean standard, but for demonstration purposes,
# a utility in squid-py is used to generate a sample Meta Data dictionary.

#%%
# Get a simple example of a Meta Data object from the library directly
metadata = squid_py.ddo.metadata.Metadata.get_example()
print('Name of asset:', metadata['base']['name'])

#%% [markdown]
# ### Section 3: Get the Service Execution Agreement (SEA) template for an Asset
# (An asset is consumed by simple download of files, such as datasets)
#%%
# TODO: The following cells are too complicated for end-users, need to refactor to simple .register_dataset(Asset, Price)
# Get the path of the SEA
SEA_template_path = squid_py.service_agreement.utils.get_sla_template_path()

# Get the ID of this SEA
template_id = squid_py.service_agreement.utils.register_service_agreement_template(
    publisher.ocn.keeper.service_agreement,
    publisher.ocn.keeper.contract_path,
    publisher.ocn.main_account,
    squid_py.service_agreement.service_agreement_template.ServiceAgreementTemplate.from_json_file(SEA_template_path)
)
print("Template ID:", template_id)

#%% [markdown]
# ### Section 4: Confirm your service endpoints with Brizo (services handler for Publishers)
#%%

brizo_url = publisher.ocn.config.get('resources', 'brizo.url')

brizo_base_url = '/api/v1/brizo'
purchase_endpoint = '{}{}/services/access/initialize'.format(brizo_url, brizo_base_url)
service_endpoint = '{}{}/services/consume'.format(brizo_url, brizo_base_url)
print("Endpoints:")
print("purchase_endpoint:", purchase_endpoint)
print("service_endpoint:", service_endpoint)

# A service descriptor function is used to build a service
this_service_desc = squid_py.service_agreement.service_factory.ServiceDescriptor.access_service_descriptor

# %% [markdown]
# In this case, the service will have a type of:
#
# `ServiceTypes.ASSET_ACCESS`
#
# And needs to be instantiated with the following attributes:
#
# `price, purchase_endpoint, service_endpoint, timeout, template_id`

publisher.ocn.keeper.web3.personal.unlockAccount(publisher.account.address, publisher.account.password)

#%%
# Register this asset into Ocean
ddo = publisher.ocn.register_asset(
    metadata, publisher.ocn.main_account.address,
    [this_service_desc(7, purchase_endpoint, service_endpoint, 360, template_id)])
print("DDO created and registered!")
print("DID:", ddo.did)
# rcpt = publisher1.account.request_tokens(5)
# publisher1.ocn._web3.eth.waitForTransactionReceipt(rcpt)
#%%
# Inspect the new DDO
print("did:", ddo.did)
manta_print.print_ddo(ddo)

