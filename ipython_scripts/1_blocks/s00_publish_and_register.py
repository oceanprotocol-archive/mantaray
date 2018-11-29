# %% [markdown]
# ## Building Blocks: Publishing assets
# In this notebook, TODO: description

# %% [markdown]
# ### Section 1: Import modules, and setup logging
#%%
import pathlib
import sys
import logging
from pathlib import Path
import squid_py
from squid_py.ocean.ocean import Ocean

# Add the local utilities package
utilities_path = Path('.') / 'script_fixtures'
if not utilities_path.exists():
    utilities_path = Path('.') / '..' / '..' / 'script_fixtures'
assert utilities_path.exists()

#Get the project root path
PATH_PROJECT_ROOT = utilities_path / '..'
PATH_PROJECT_ROOT.absolute()

utilities_path_str = str(utilities_path.absolute())
if utilities_path_str not in sys.path:
    sys.path.append(utilities_path_str)

import script_fixtures.logging as util_logging
util_logging.logger.setLevel('INFO')

import script_fixtures.user as user
logging.info("Squid API version: {}".format(squid_py.__version__))

#%%
# get_registered_ddo -> register_service_agreement_template -> get_conditions_data_from_keeper_contracts
# The data:
# contract_addresses
# fingerprints
# fulfillment_indices
# conditions_keys

# %% [markdown]
# ### Section 1: Instantiate a simulated User
#%%
# The contract addresses are loaded from file
PATH_CONFIG = pathlib.Path.cwd() / 'config_local.ini'
assert PATH_CONFIG.exists(), "{} does not exist".format(PATH_CONFIG)

ocn = Ocean(config_file=PATH_CONFIG)
print("HTTP Client:")
print(ocn._http_client)
print("Secret Store Client:")
print(ocn._secret_store_client)

# This utility function gets all simulated accounts
users = user.get_all_users(ocn.accounts)

# We don't need this ocn instance reference anymore
del ocn

# Let's take the first unlocked account, and name it the Publisher
publisher1 = [u for u in users if not u.locked][0]
publisher1.name = "Edward Teach"
publisher1.role = "Publisher"
print(publisher1)

assert publisher1.ocn._http_client.__name__ == 'requests'
assert publisher1.ocn._secret_store_client.__name__ == 'Client'

ddo = get_registered_ddo(publisher1.ocn)

#%% [markdown]
# ### Section 2: Get the template of the Service Execution Agreement
#%%
# First, get the template ID
SEA_template_path = squid_py.service_agreement.utils.get_sla_template_path()

template_id = squid_py.service_agreement.utils.register_service_agreement_template(
    publisher1.ocn.keeper.service_agreement,
    publisher1.ocn.keeper.contract_path,
    publisher1.ocn.main_account,
    squid_py.service_agreement.service_agreement_template.ServiceAgreementTemplate.from_json_file(SEA_template_path)
)

#%%

# Get a simple example of a Metadata object
metadata = squid_py.ddo.metadata.Metadata.get_example()

brizo_url = 'http://localhost:8030' # For now, this is hardcoded
# TODO: Discussion on whether Squid should have an API to Brizo?

brizo_base_url = '/api/v1/brizo'
purchase_endpoint = '{}{}/services/access/initialize'.format(brizo_url, brizo_base_url)
service_endpoint = '{}{}/services/consume'.format(brizo_url, brizo_base_url)

ddo = publisher1.ocn.register_asset(
    metadata, publisher1.ocn.main_account.address,
    [ServiceDescriptor.access_service_descriptor(7, purchase_endpoint, service_endpoint, 360, template_id)]
)