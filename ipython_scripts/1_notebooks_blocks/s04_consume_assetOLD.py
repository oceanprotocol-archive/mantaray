# %% [markdown]
# Getting Underway - Downloading Datasets (Assets)

# %% [markdown]
# ### Section 0: Import modules, and setup logging

#%%
# Standard imports
import logging
from pprint import pprint
import os
import time
from pathlib import Path
import random
# Import mantaray and the Ocean API (squid)
import squid_py
from squid_py import Metadata
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
from squid_py.agreements.service_agreement import ServiceAgreement
from squid_py.agreements.service_types import ServiceTypes
import mantaray_utilities as manta_utils
from squid_py.keeper.web3_provider import Web3Provider
# Setup logging
from mantaray_utilities.user import password_map
manta_utils.logging.logger.setLevel('INFO')

print("squid-py Ocean API version:", squid_py.__version__)

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
#%% Register an asset
path_passwords = manta_utils.config.get_project_path() / 'passwords.csv'
passwords = manta_utils.user.load_passwords(path_passwords)

publisher_acct = random.choice([acct for acct in ocn.accounts.list() if password_map(acct.address, passwords)])
publisher_acct.password = password_map(publisher_acct.address, passwords)
assert publisher_acct.password
ddo = ocn.assets.create(Metadata.get_example(), publisher_acct)


#%%
# Get a consumer account
path_passwords = manta_utils.config.get_project_path() / 'passwords.csv'
passwords = manta_utils.user.load_passwords(path_passwords)

consumer_acct = random.choice([acct for acct in ocn.accounts.list() if password_map(acct.address, passwords)])
consumer_acct.password = password_map(consumer_acct.address, passwords)
assert consumer_acct.password
print("Consumer account address: ", consumer_acct.address)

#%% NEW FLOW
service = ddo.get_service(service_type=ServiceTypes.ASSET_ACCESS)
sa = ServiceAgreement.from_service_dict(service.as_dictionary())

agreement_id = ocn.assets.order(
        ddo.did, sa.service_definition_id, consumer_acct)
logging.info("Agreement ID:{}".format(agreement_id))
logging.info("Sleep".format())
time.sleep(30)
ocn.assets.consume(
    agreement_id,
    ddo.did,
    sa.service_definition_id,
    consumer_acct,
    ocn._config.downloads_path)
logging.info('Success buying asset.')

#%% [markdown]
# ### Section 2: Find an asset
#%%
# # Use the Query function to get all existing assets
# basic_query = {"query":{"text":["Weather"]}}
# all_ddos = ocn.assets.query(basic_query)
# assert len(all_ddos), "There are no assets registered, go to s03_publish_and_register!"
# print("There are {} assets registered in the metadata store.".format(len(all_ddos)))
#
# assert len(all_ddos), "There are no assets registered, go to s03_publish_and_register!"
#
# # Get a DID for testing
# selected_did = all_ddos[-1].did
# print("Selected DID:",selected_did)

#%% [markdown]
# Or alternatively, since the asset may be registered but not actually exist in Aquarius, you can
# specify the asset below (i.e. the DID of the asset you previously registered)
#%%

# selected_did = "did:op:513fd16ffa854bf8a62c32ebd6f2f0933c39a45cde0346fdb864634c5dd849d7"
#%% An Asset (DDO) can be also be resolved from a DID

this_asset = ocn.assets.resolve(selected_did)

#pprint(this_asset)
print(this_asset.metadata['base']['name'])
print("Price:", this_asset.metadata['base']['price'])

# %% [markdown]
# Your account will need some Ocean Token to make real transactions
# %%
if ocn.accounts.balance(consumer_acct).ocn == 0:
    ocn.accounts.request_tokens(consumer_acct, 100)
# %% [markdown]
# Purchase the Asset!
# %%
manta_utils.logging.logger.setLevel('INFO')
service_agreement_id = ocn.assets.order(this_asset.did, 'Access', consumer_acct)
print('New service agreement id:', service_agreement_id)
print('Waiting for blockchain transaction....')
time.sleep(30)
ocn.assets.consume(
    service_agreement_id,
    this_asset.did,
    'Access',
    consumer_acct,
    ocn._config.downloads_path)
logging.info('Success buying asset.')

# %% [markdown]
# The asset download is automatically initiated, this will take time to complete! There are several events
# emitted by the blockchain node to show the progress of the transaction and fulfilled conditions.
#%%
# def _log_event(event_name):
#     def _process_event(event):
#         print(f'Received event {event_name}: {event}')
#
#     return _process_event
#
# event = ocn._keeper.escrow_access_secretstore_template.subscribe_agreement_created(
#     service_agreement_id,
#     100,
#     _log_event(ocn._keeper.escrow_access_secretstore_template.AGREEMENT_CREATED_EVENT),
#     (),
#     wait=True
# )
# assert event, 'no event for EscrowAccessSecretStoreTemplate.AgreementCreated'
#
# event = keeper.lock_reward_condition.subscribe_condition_fulfilled(
#     service_agreement_id,
#     100,
#     _log_event(ocn._keeper.lock_reward_condition.FULFILLED_EVENT),
#     (),
#     wait=True
# )
# assert event, 'no event for LockRewardCondition.Fulfilled'
#
# event = keeper.escrow_reward_condition.subscribe_condition_fulfilled(
#     service_agreement_id,
#     100,
#     _log_event(ocn._keeper.escrow_reward_condition.FULFILLED_EVENT),
#     (),
#     wait=True
# )
# assert event, 'no event for EscrowReward.Fulfilled'
#
# ocn.agreements.is_access_granted(service_agreement_id, ddo.did, consumer_account.address)
#
# assert event, 'No event received for ServiceAgreement Fulfilled.'
# logging.info('Success buying asset.')


# %%
asset_path = Path.cwd() / ocn._config.downloads_path / f'datafile.{this_asset.asset_id}.0'
print("Check for your downloaded asset in", asset_path)
print("This might not appear immediately - the transaction needs be mined and the download needs to complete!")
