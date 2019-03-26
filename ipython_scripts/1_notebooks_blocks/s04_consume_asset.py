# %% [markdown]
# Getting Underway - Downloading Datasets (Assets)
# To complete the basic datascience workflow, this notebook will demonstrate how a user
# can download an asset. Downloading an asset is a simple example of a Service Execution Agreement -
# similar to a contract with a series of clauses. Each clause is secured on the blockchain, allowing for trustful
# execution of a contract.
#
# In this notebook, an asset will be first published as before, and then ordered and downloaded.

#%%
import logging
import os
from squid_py import Metadata, Ocean
import squid_py
import mantaray_utilities as manta_utils

# Setup logging
from mantaray_utilities.user import get_account_from_config
from mantaray_utilities.blockchain import subscribe_event
manta_utils.logging.logger.setLevel('INFO')
import mantaray_utilities as manta_utils
from squid_py import Config
from squid_py.keeper import Keeper
from pathlib import Path
import datetime
#%% Add a file  handler
path_log_file = Path.home() / '{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
fh = logging.FileHandler(path_log_file)
fh.setLevel(logging.DEBUG)
manta_utils.logging.logger.addHandler(fh)
# %% [markdown]
# Get the configuration from the INI file
#%%
CONFIG_INI_PATH = manta_utils.config.get_config_file_path()
logging.critical("Deployment type: {}".format(manta_utils.config.get_deployment_type()))
logging.critical("Configuration file selected: {}".format(CONFIG_INI_PATH))
logging.critical("Squid API version: {}".format(squid_py.__version__))
config_from_ini = Config(CONFIG_INI_PATH)

#%%
ocn = Ocean(config_from_ini)
keeper = Keeper.get_instance()

# %% [markdown]
# Get Publisher account, and register an asset for testing

#%%
publisher_account = get_account_from_config(config_from_ini, 'parity.address', 'parity.password')
print("Publisher address: {}".format(publisher_account.address))
print("Publisher   ETH: {:0.1f}".format(ocn.accounts.balance(publisher_account).eth/10**18))
print("Publisher OCEAN: {:0.1f}".format(ocn.accounts.balance(publisher_account).ocn/10**18))

#%%
# Register an asset
ddo = ocn.assets.create(Metadata.get_example(), publisher_account)
logging.info(f'registered ddo: {ddo.did}')

# %% [markdown]
# Get Consumer account
#%%
consumer_account = get_account_from_config(config_from_ini, 'parity.address1', 'parity.password1')
print("Consumer address: {}".format(consumer_account.address))
print("Consumer   ETH: {:0.1f}".format(ocn.accounts.balance(consumer_account).eth/10**18))
print("Consumer OCEAN: {:0.1f}".format(ocn.accounts.balance(consumer_account).ocn/10**18))
assert ocn.accounts.balance(consumer_account).eth/10**18 > 1, "Insuffient ETH in account {}".format(consumer_account.address)
# Ensure the consumer always has 10 OCEAN
if ocn.accounts.balance(consumer_account).ocn/10**18 < 10:
    refill_amount = 10 - ocn.accounts.balance(consumer_account).ocn/10**18 < 10
    ocn.accounts.request_tokens(consumer_account, refill_amount)

# %% [markdown]
# Initiate the agreement for accessing (downloading) the asset
#%%
agreement_id = ocn.assets.order(ddo.did, 'Access', consumer_account)
logging.info("Consumer has placed an order for asset {}".format(ddo.did))
logging.info("The service agreement ID is {}".format(agreement_id))

# %% [markdown]
# In Ocean Protocol, downloading an asset is enforced by a contract.
# The contract conditions and clauses are set by the publisher. Conditions trigger events, which are monitored
# to ensure the contract is successfully executed.
#%%
# Listen to events in the download process
subscribe_event("created agreement", keeper, agreement_id)
subscribe_event("lock reward", keeper, agreement_id)
subscribe_event("access secret store", keeper, agreement_id)
subscribe_event("escrow reward", keeper, agreement_id)

# %% [markdown]
# Now that the agreement is signed, the consumer can download the asset.
#%%

assert ocn.agreements.is_access_granted(agreement_id, ddo.did, consumer_account.address)

ocn.assets.consume(agreement_id, ddo.did, 'Access', consumer_account, 'downloads_nile')
logging.info('Success buying asset.')

#%%



