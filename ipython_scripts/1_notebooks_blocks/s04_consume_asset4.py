
import logging
import os
os.environ['USE_K8S_CLUSTER'] = '1'
from squid_py import ConfigProvider, Metadata, Ocean
import time
import squid_py

import mantaray_utilities as manta_utils
from squid_py.keeper.web3_provider import Web3Provider
# Setup logging
from mantaray_utilities.user import password_map
manta_utils.logging.logger.setLevel('INFO')
import mantaray_utilities as manta_utils
from squid_py.accounts.account import Account
from squid_py.agreements.service_agreement import ServiceAgreement
from squid_py.agreements.service_types import ServiceTypes
from squid_py import Config

# import keeper


#%%
CONFIG_INI_PATH = manta_utils.config.get_config_file_path()
logging.critical("Deployment type: {}".format(manta_utils.config.get_deployment_type()))
logging.critical("Configuration file selected: {}".format(CONFIG_INI_PATH))
logging.critical("Squid API version: {}".format(squid_py.__version__))
config_from_ini = Config(CONFIG_INI_PATH)

# %% [markdown]
# Until things are more stable, the following cell performs some sanity checks on versions

#%%
# Assert versions
import pip_api
import json
from pathlib import Path

version_kc_installed = 'v'+str(pip_api.installed_distributions()['keeper-contracts'].version)
network_name = 'nile'
folder_artifacts = config_from_ini.get('keeper-contracts', 'keeper.path')
path_artifacts = Path.cwd() / folder_artifacts
assert path_artifacts.exists()
for path_artifact_file in path_artifacts.glob("*.{}.json".format(network_name)):
    with open(path_artifact_file) as fp:
        artifact_dict = json.load(fp)
    assert artifact_dict['version'] == version_kc_installed, \
        "Version mismatch, {} {}".format(artifact_dict['version'], version_kc_installed)
logging.info("Contract ABI and installed version {} confirmed".format(version_kc_installed))



#%% get_account_from_config
from squid_py.accounts.account import Account
from squid_py.keeper import Keeper
from squid_py.keeper.web3_provider import Web3Provider

def get_account_from_config(config, config_account_key, config_account_password_key):
    address = config.get('keeper-contracts', config_account_key)
    address = Web3Provider.get_web3().toChecksumAddress(address)
    password = config.get('keeper-contracts', config_account_password_key)
    return Account(address, password)

#%%
def _log_event(event_name):
    def _process_event(event):
        print(f'Received event {event_name}.')

    return _process_event

# #%% get_publisher_account
# def get_publisher_account(config):
#     acc = get_account_from_config(config, 'parity.address', 'parity.password')
#     if acc is None:
#         acc = Account(Keeper.get_instance().accounts[0])
#     return acc

#
#%%
# config_from_dict = Config(options_dict=config_dict2)
#
# # config = config_from_dict

config = config_from_ini

# ConfigProvider.set_config(config)
ocn = Ocean(config_from_ini)
keeper = Keeper.get_instance()
#%%
# Get Publisher account
# publisher_account = get_publisher_account(config)
publisher_account = get_account_from_config(config, 'parity.address', 'parity.password')
if not publisher_account:
    publisher_account = ([acc for acc in ocn.accounts.list() if acc.password] or ocn.accounts.list())[0]
print("Publisher address: {}".format(publisher_account.address))
print("Publisher   ETH: {:0.1f}".format(ocn.accounts.balance(publisher_account).eth/10**18))
print("Publisher OCEAN: {:0.1f}".format(ocn.accounts.balance(publisher_account).ocn/10**18))

#%%
# Register an asset
ddo = ocn.assets.create(Metadata.get_example(), publisher_account)
logging.info(f'registered ddo: {ddo.did}')

#%%

consumer_account = get_account_from_config(config, 'parity.address1', 'parity.password1')
print("Consumer address: {}".format(publisher_account.address))
print("Consumer   ETH: {:0.1f}".format(ocn.accounts.balance(publisher_account).eth/10**18))
print("Consumer OCEAN: {:0.1f}".format(ocn.accounts.balance(publisher_account).ocn/10**18))


#%%

service = ddo.get_service(service_type=ServiceTypes.ASSET_ACCESS)
# cons_ocn.accounts.request_tokens(consumer_account, 100)
# ocn.accounts.request_tokens(consumer_account, 100)
sa = ServiceAgreement.from_service_dict(service.as_dictionary())

agreement_id = ocn.assets.order(
    ddo.did, 'Access', consumer_account)
logging.info('placed order: %s, %s', ddo.did, agreement_id)

#%%
event = keeper.escrow_access_secretstore_template.subscribe_agreement_created(
    agreement_id,
    60,
    _log_event(keeper.escrow_access_secretstore_template.AGREEMENT_CREATED_EVENT),
    (),
    wait=True
)
assert event, 'no event for EscrowAccessSecretStoreTemplate.AgreementCreated'

event = keeper.lock_reward_condition.subscribe_condition_fulfilled(
    agreement_id,
    60,
    _log_event(keeper.lock_reward_condition.FULFILLED_EVENT),
    (),
    wait=True
)
assert event, 'no event for LockRewardCondition.Fulfilled'

event = keeper.access_secret_store_condition.subscribe_condition_fulfilled(
    agreement_id,
    60,
    _log_event(keeper.escrow_reward_condition.FULFILLED_EVENT),
    (),
    wait=True
)
assert event, 'no event for AccessSecretStoreCondition.Fulfilled'

event = keeper.escrow_reward_condition.subscribe_condition_fulfilled(
    agreement_id,
    60,
    _log_event(keeper.escrow_reward_condition.FULFILLED_EVENT),
    (),
    wait=True
)
assert event, 'no event for EscrowReward.Fulfilled'
assert ocn.agreements.is_access_granted(agreement_id, ddo.did, consumer_account.address)

ocn.assets.consume(
    agreement_id,
    ddo.did,
    'Access',
    consumer_account,
    "downloads_nile")
logging.info('Success buying asset.')


