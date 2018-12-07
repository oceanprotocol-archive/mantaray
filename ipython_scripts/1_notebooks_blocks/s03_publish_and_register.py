# %% [markdown]
# ## Building Blocks: Publishing assets
# In this notebook, TODO: description

# %% [markdown]
# ### Section 0: Import modules, and setup logging

#%%
# Standard imports
import logging
from pathlib import Path

# Import mantaray and the Ocean API (squid)
import squid_py
from squid_py.ocean.ocean import Ocean
import mantaray_utilities.config as manta_config
import mantaray_utilities.logging as manta_logging
import mantaray_utilities.user as manta_user
import mantaray_utilities.asset_pretty_print as manta_print

# Setup logging
manta_logging.logger.setLevel('INFO')

#%%
# Get the configuration file path for this environment
CONFIG_INI_PATH = manta_config.get_config_file_path()

logging.info("Configuration file selected: {}".format(CONFIG_INI_PATH))
logging.info("Squid API version: {}".format(squid_py.__version__))

# %% [markdown]
# ### Section 1: Instantiate a simulated User
# A 'User' in an abstract class representing a user of Ocean Protocol
#
# Follow the most notorious pirate Edward Teach (Blackbeard) as he tries to register an asset into Ocean Protocol
# <a title="Engraved by Benjamin Cole (1695–1766) [Public domain], via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File:Bbeard_Sword.jpg"><img width="256" alt="Bbeard Sword" src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Bbeard_Sword.jpg/256px-Bbeard_Sword.jpg"></a>
#%%
# Instantiate Ocean with the default configuration file

ocn = Ocean(config_file=CONFIG_INI_PATH)
#%%
print("HTTP Client:", ocn._http_client.__name__)
print("Secret Store Client:", ocn._secret_store_client)

#%% [markdown]
# For this tutorial, we will select one of the available unlocked accounts
#
# In general, as a publisher, you will have your own configuration file with your personal account.

#%%
# This utility function gets all simulated accounts
users = manta_user.get_all_users(ocn.accounts)

# We don't need this ocn instance reference anymore
del ocn

# Let's take the first unlocked account, and name it the Publisher
publisher1 = [u for u in users if not u.locked][0]
publisher1.name = "Edward Teach"
publisher1.role = "Publisher"
print(publisher1)

assert publisher1.ocn._http_client.__name__ == 'requests'
assert publisher1.ocn._secret_store_client.__name__ == 'Client'

#%% [markdown]
# ### Section 2: Create your MetaData for your asset
# A more complex use case is to manually generate your metadata conforming to Ocean standard

#%%
# Get a simple example of a Metadata object from the library directly
metadata = squid_py.ddo.metadata.Metadata.get_example()
print('Name of asset:', metadata['base']['name'])

#%% [markdown]
# ### Section 3: Get the Service Execution Agreement (SEA) template for an Asset
# (An asset is consumed by simple download of files, such as datasets)
#%%
# Get the path of the SEA
SEA_template_path = squid_py.service_agreement.utils.get_sla_template_path()

# Get the ID of this SEA
template_id = squid_py.service_agreement.utils.register_service_agreement_template(
    publisher1.ocn.keeper.service_agreement,
    publisher1.ocn.keeper.contract_path,
    publisher1.ocn.main_account,
    squid_py.service_agreement.service_agreement_template.ServiceAgreementTemplate.from_json_file(SEA_template_path)
)
print(template_id)

#%% [markdown]
# ### Section X: Confirm your service endpoints with Brizo (services handler for Publishers)
#%%
# brizo_url = 'http://172.15.0.17:8030' # For now, this is hardcoded
brizo_url = publisher1.ocn.config.get('resources','brizo.url')
# TODO: Discussion on whether Squid should have an API to Brizo?



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

#%%
# Register this asset into Ocean
ddo = publisher1.ocn.register_asset(
    metadata, publisher1.ocn.main_account.address,
    [this_service_desc(7, purchase_endpoint, service_endpoint, 360, template_id)]
)
print("DDO created and registered!")
#%%
# Inspect the new DDO
print("did:", ddo.did)
manta_print.print_ddo(ddo)

