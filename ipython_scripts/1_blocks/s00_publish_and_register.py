# %% [markdown]
# ## Building Blocks: Publishing assets
# In this notebook, TODO: description

# %% [markdown]
# ### Section 0: Housekeeping, import modules, and setup logging
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

# %% [markdown]
# ### Section 1: Instantiate a simulated User
# A 'User' in an abstract class representing a user of Ocean Protocol
#
# Follow the most notorious pirate Edward Teach (Blackbeard) as he tries to register an asset into Ocean Protocol
# <a title="Engraved by Benjamin Cole (1695–1766) [Public domain], via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File:Bbeard_Sword.jpg"><img width="256" alt="Bbeard Sword" src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Bbeard_Sword.jpg/256px-Bbeard_Sword.jpg"></a>
#%%
# The contract addresses are loaded from file
PATH_CONFIG = pathlib.Path.cwd() / 'config_local.ini'
assert PATH_CONFIG.exists(), "{} does not exist".format(PATH_CONFIG)

ocn = Ocean(config_file=PATH_CONFIG)
#%%
print("HTTP Client:")
print(ocn._http_client)
print("Secret Store Client:")
print(ocn._secret_store_client)

#%%
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

#%% [markdown]
# ### Section 2: Create your MetaData for your asset
# A more complex use case is to manually generate your metadata conforming to Ocean standard
# Metadata is a dictionary, as follows:

#%%
# Get a simple example of a Metadata object from the library directly
metadata = squid_py.ddo.metadata.Metadata.get_example()
print('Name of asset:',metadata['base']['name'])

#%% [markdown]
# ### Section X: Get the Service Execution Agreement (SEA) template for an Asset
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
brizo_url = 'http://localhost:8030' # For now, this is hardcoded
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
print("Services:")
for svc in ddo.services:
    if 'conditions' in svc._values:
        num_conditions = len(svc._values['conditions'])
    else:
        num_conditions = 0
    print("\t{} service with {} conditions".format(svc._type,num_conditions))
    if 'conditions' in svc._values:
        for condition in svc._values['conditions']:
            params = [p.name for p in condition.parameters]
            param_string = ", ".join(params)
            print("\t\t{}.{}({})".format(condition.contract_name,condition.function_name,param_string))


