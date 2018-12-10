# %% [markdown]
# ## Building Blocks: Downloading Datasets
# In this notebook, TODO: description

# %% [markdown]
# ### Section 0: Import modules, and setup logging

#%%
# Standard imports
import sys
import logging
import requests
import json
import time
from web3 import Web3

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
logging.info("Deployment type: {}".format(manta_config.get_deployment_type()))
logging.info("Configuration file selected: {}".format(CONFIG_INI_PATH))
logging.info("Squid API version: {}".format(squid_py.__version__))

# %% [markdown]
# ### Section 1: Instantiate a simulated User
# A 'User' in an abstract class representing a user of Ocean Protocol
#
# Follow Anne Bonny as she purchases an asset which has been registered in Ocean Protocol
#%%
ocn = Ocean(config_file=CONFIG_INI_PATH)

#%%
# This utility function gets all simulated accounts
users = manta_user.get_all_users(ocn.accounts)

# We don't need this ocn instance reference anymore
del ocn

# Let's take the first unlocked account, and name it the Consumer
consumer1 = [u for u in users if not u.locked][0]
consumer1.name = "Anny Bonny"
consumer1.role = "Consumer"
print(consumer1)

assert consumer1.ocn._http_client.__name__ == 'requests'
assert consumer1.ocn._secret_store_client.__name__ == 'Client'
assert consumer1.account.ocean_balance > 0, "Consumer does not have any Ocean token, go to 'users_and_token' script and fund the account!"
#%% [markdown]
# ### Section 2: Find an asset
#%%
# Get ALL dids
result = requests.get(consumer1.ocn.metadata_store._base_url).content
all_dids = json.loads(result)['ids']
assert len(all_dids) > 0

# Get the DID for testing
first_did = all_dids[-1]

#%% From this DID, get the DDO
this_ddo = consumer1.ocn.resolve_did(first_did)
manta_print.print_ddo(this_ddo)

#%%
# Skip this cell...
# TODO: This is broken, wait for patch in squid_py to point to correct method (resolve_did())
# consumer1.ocn.get_asset(first_did)
#%%
# TODO: Remove this in final publication
# The asset can also be retreieved direct from the REST endpoint
# this_asset_endpoint = consumer1.ocn.metadata_store._base_url  + '/ddo/' + first_did
# result = requests.get(this_asset_endpoint).content
# ddo_dict = json.loads(result)

#%% [markdown]
# ### Section 3: Get ready for purchase
#%%

# Get the service agreement for consuming (downloading)
service_types = squid_py.service_agreement.service_types.ServiceTypes
service = this_ddo.get_service(service_type=service_types.ASSET_ACCESS)
assert squid_py.service_agreement.service_agreement.ServiceAgreement.SERVICE_DEFINITION_ID_KEY in service.as_dictionary()

# This is the Service Agreement for downloading the Asset, contains conditions
sa = squid_py.service_agreement.service_agreement.ServiceAgreement.from_service_dict(service.as_dictionary())

consumer_address = consumer1.ocn.main_account.address

# The purchase (sign) command will fail unless the account has some Ocean Token to spend!
if consumer1.account.ocean_balance == 0:
    rcpt = consumer1.account.request_tokens(10)
    consumer1.ocn._web3.eth.waitForTransactionReceipt(rcpt)


#%% [markdown]
# ### Section 3: Execute the agreement (purchase!)
#%%
# This will send the purchase request to Brizo which in turn will execute the agreement on-chain
# this_did = 'did:op:0x23d76f6f5e1040c8bba8701fdaa59e28bf2c9edd3acc400aa8af46fe1433344e'
this_did = this_ddo.did
service_agreement_id = consumer1.ocn.sign_service_agreement(this_did, sa.sa_definition_id, consumer_address)
print('got new service agreement id:', service_agreement_id)

#%%
# TODO: This has been refactored. The workflow is now part of .sign_service_agreement() call. Delete cell.
# We will now watch on-chain to ensure that the service is 1) Executed and 2) Granted
#
# def wait_for_event(event, arg_filter, wait_iterations=20):
#     _filter = event.createFilter(fromBlock=0 , argument_filters=arg_filter)
#     for check in range(wait_iterations):
#         events = _filter.get_all_entries()
#         if events:
#             return events[0]
#         time.sleep(0.5)
#
#
# filter1 = {'serviceAgreementId': Web3.toBytes(hexstr=service_agreement_id)}
# filter_2 = {'serviceId': Web3.toBytes(hexstr=service_agreement_id)}
#
# executed = wait_for_event(consumer1.ocn.keeper.service_agreement.events.ExecuteAgreement, filter1)
# assert executed
# granted = wait_for_event(consumer1.ocn.keeper.access_conditions.events.AccessGranted, filter_2)
# assert granted
# fulfilled = wait_for_event(consumer1.ocn.keeper.service_agreement.events.AgreementFulfilled, filter1)
# assert fulfilled
# time.sleep(3)