# %% [markdown]
# export USE_K8S_CLUSTER=true
# export DOCKER_START_TIME=now
# export DOCKER_END_TIME=20:00
# export DOCKER_INTERVAL=30
# export PARITY_ADDRESS=0x413c9BA0A05B8A600899B41b0c62dd661e689354
# export PARITY_PASSWORD=ocean_secret
# export PARITY_KEY_FILE=/path/to/publisher/keyfile.json
# export PARITY_ADDRESS1=0x06C0035fE67Cce2B8862D63Dc315D8C8c72207cA
# export PARITY_PASSWORD1=ocean_secret
# export PARITY_KEY_FILE1=/path/to/consumer/keyfile.json

#%%
import json
import logging
import os

from ocean_keeper import Keeper
from ocean_keeper.utils import get_account
from ocean_utils.agreements.service_types import ServiceTypes
from squid_py import Ocean
import squid_py
import mantaray_utilities as manta_utils

# Setup logging
from mantaray_utilities.blockchain import subscribe_event
manta_utils.logging.logger.setLevel('INFO')
import mantaray_utilities as manta_utils
from squid_py import Config
from pathlib import Path
import datetime

#%% Set environment
os.environ['USE_K8S_CLUSTER']='true'

#%% Add a file  handler
path_log_file = Path('/test_logs') / '{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
fh = logging.FileHandler(path_log_file)
fh.setLevel(logging.DEBUG)
manta_utils.logging.logger.addHandler(fh)
logging.info("Log file at: {}".format(path_log_file))
# %% [markdown]
# Get the configuration from the INI file
#%%
CONFIG_INI_PATH = manta_utils.config.get_config_file_path()
logging.critical("Deployment type: {}".format(manta_utils.config.get_deployment_type()))
logging.critical("Configuration file selected: {}".format(CONFIG_INI_PATH))
logging.critical("Squid API version: {}".format(squid_py.__version__))
logging.critical("Mantaray Utilities version: {}".format(manta_utils.__version__))

config_from_ini = Config(CONFIG_INI_PATH)

#%%
ocn = Ocean(config_from_ini)
keeper = Keeper.get_instance()

#%%
# DOCKER_STRICT = False
DOCKER_STRICT = True  # Strictly enforce the environment variables
if DOCKER_STRICT:
    assert 'PARITY_ADDRESS' in os.environ
    assert 'PARITY_PASSWORD' in os.environ
    assert 'PARITY_KEY_FILE' in os.environ
    assert 'PARITY_ADDRESS1' in os.environ
    assert 'PARITY_PASSWORD1' in os.environ
    assert 'PARITY_KEY_FILE1' in os.environ

# %% [markdown]
# Get Publisher account, and register an asset for testing

#%%
# Get account from env vars: PARITY_ADDRESS, PARITY_PASSWORD, PARITY_KEY_FILE
publisher_account = get_account(0)

print("Publisher address: {}".format(publisher_account.address))
print("Publisher   ETH: {:0.1f}".format(ocn.accounts.balance(publisher_account).eth/10**18))
print("Publisher OCEAN: {:0.1f}".format(ocn.accounts.balance(publisher_account).ocn/10**18))

#%%
# Register an asset
metadata_path = 'assets/sample_metadata.json'
with open(metadata_path, 'w') as f:
    metadata = json.load(f)

ddo = ocn.assets.create(metadata, publisher_account)
logging.info(f'registered ddo: {ddo.did}')

# %% [markdown]
# Get Consumer account
#%%
# Get account from env vars: PARITY_ADDRESS1, PARITY_PASSWORD1, PARITY_KEY_FILE1
consumer_account = get_account(1)
print("Consumer address: {}".format(consumer_account.address))
print("Consumer   ETH: {:0.1f}".format(ocn.accounts.balance(consumer_account).eth/10**18))
print("Consumer OCEAN: {:0.1f}".format(ocn.accounts.balance(consumer_account).ocn/10**18))
assert (ocn.accounts.balance(consumer_account).eth/10**18) > 1, "Insuffient ETH in account {}".format(consumer_account.address)
# Ensure the consumer always has 10 OCEAN
if (ocn.accounts.balance(consumer_account).ocn/10**18) < 10:
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

ocn.assets.consume(agreement_id, ddo.did, ServiceTypes.ASSET_ACCESS, consumer_account, 'downloads_nile')
logging.info('Success buying asset.')
