
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
#%%
CONFIG_INI_PATH = manta_utils.config.get_config_file_path()
logging.critical("Deployment type: {}".format(manta_utils.config.get_deployment_type()))
logging.critical("Configuration file selected: {}".format(CONFIG_INI_PATH))
logging.critical("Squid API version: {}".format(squid_py.__version__))
config_from_ini = Config(CONFIG_INI_PATH)

#%% get_account_from_config
from squid_py.accounts.account import Account
from squid_py.keeper import Keeper
from squid_py.keeper.web3_provider import Web3Provider

def get_account_from_config(config, config_account_key, config_account_password_key):
    address = None
    if config.has_option('keeper-contracts', config_account_key):
        address = config.get('keeper-contracts', config_account_key)
        address = Web3Provider.get_web3().toChecksumAddress(address) if address else None

    if not (address and address in Keeper.get_instance().accounts):
        return None

    password = None
    if address and config.has_option('keeper-contracts', config_account_password_key):
        password = config.get('keeper-contracts', config_account_password_key)

    return Account(address, password)

#%%
def _log_event(event_name):
    def _process_event(event):
        print(f'Received event {event_name}.')

    return _process_event

#%% get_publisher_account
def get_publisher_account(config):
    acc = get_account_from_config(config, 'parity.address', 'parity.password')
    if acc is None:
        acc = Account(Keeper.get_instance().accounts[0])
    return acc

#%%
# from squid_py import Config
# class ExampleConfig:
#     environment = 'TEST_NILE'
#     config_dict = {
#         "keeper-contracts": {
#             "keeper.url": "https://nile.dev-ocean.com",
#             "keeper.path": "artifacts",
#             "secret_store.url": "https://secret-store.dev-ocean.com",
#             "parity.url": "https://nile.dev-ocean.com",
#             "parity.address": "0x413c9ba0a05b8a600899b41b0c62dd661e689354",
#             "parity.password": "ocean_secret",
#             "parity.address1": "0x1322A6ef2c560107733bFc622Fe556961Cb430a5",
#             "parity.password1": "ocean_secret"
#         },
#         "resources": {
#             "aquarius.url": "https://nginx-aquarius.dev-ocean.com/",
#             "brizo.url": "https://nginx-brizo.dev-ocean.com/",
#             "storage.path": "squid_py.db",
#             "downloads.path": "consume-downloads"
#         }
#     }
#     def get_config():
#         logging.info("Configuration loaded for environment '{}'".format(ExampleConfig.environment))
#         return Config(options_dict=ExampleConfig.config_dict)
# #%%
# config_dict = {
#     "keeper-contracts": {
#         "keeper.url": "https://nile.dev-ocean.com",
#         "keeper.path": "artifacts",
#         "secret_store.url": "https://secret-store.dev-ocean.com",
#         "parity.url": "https://nile.dev-ocean.com",
#         "parity.address": "0x413c9ba0a05b8a600899b41b0c62dd661e689354",
#         "parity.password": "ocean_secret",
#         "parity.address1": "0x1322A6ef2c560107733bFc622Fe556961Cb430a5",
#         "parity.password1": "ocean_secret"
#     },
#     "resources": {
#         "aquarius.url": "https://nginx-aquarius.dev-ocean.com/",
#         "brizo.url": "https://nginx-brizo.dev-ocean.com/",
#         "storage.path": "squid_py.db",
#         "downloads.path": "consume-downloads"
#     }
# }
#
#
# config_dict2 = {
#     "keeper-contracts" : {
#         "keeper.url" : "https://nile.dev-ocean.com",
#         "keeper.path" : "artifacts_nile",
#         "secret_store.url" : "https://secret-store.dev-ocean.com",
#         "parity.url" : "https://nile.dev-ocean.com",
#         "parity.address" : "0x413c9BA0A05B8A600899B41b0c62dd661e689354",
#         "parity.password" : "ocean_secret",
#         "parity.address1" : "0x1322A6ef2c560107733bFc622Fe556961Cb430a5",
#         "parity.password1" : "ocean_secret",
#     },
#     "resources" : {
#         "aquarius.url" : "https://nginx-aquarius.dev-ocean.com/",
#         "brizo.url" : "https://nginx-brizo.dev-ocean.com/",
#         "storage.path" : "squid_py.db",
#         "downloads.path" : "downloads_nile",
#         }
# }
#
#%%
# config_from_dict = Config(options_dict=config_dict2)
#
# # config = config_from_dict

config = config_from_ini

ConfigProvider.set_config(config)
ocn = Ocean()
acc = get_publisher_account(config)
if not acc:
    acc = ([acc for acc in ocn.accounts.list() if acc.password] or ocn.accounts.list())[0]

ddo = ocn.assets.create(Metadata.get_example(), acc)
logging.info(f'registered ddo: {ddo.did}')

#%%
keeper = Keeper.get_instance()
cons_ocn = Ocean()
# cons_ocn = Ocean(configuration)
consumer_account = get_account_from_config(config, 'parity.address1', 'parity.password1')

#%%

# sign agreement using the registered asset did above
service = ddo.get_service(service_type=ServiceTypes.ASSET_ACCESS)
# This will send the purchase request to Brizo which in turn will execute the agreement on-chain
cons_ocn.accounts.request_tokens(consumer_account, 100)
sa = ServiceAgreement.from_service_dict(service.as_dictionary())

agreement_id = cons_ocn.assets.order(
    ddo.did, sa.service_definition_id, consumer_account)
logging.info('placed order: %s, %s', ddo.did, agreement_id)

event = keeper.escrow_access_secretstore_template.subscribe_agreement_created(
    agreement_id,
    30,
    _log_event(keeper.escrow_access_secretstore_template.AGREEMENT_CREATED_EVENT),
    (),
    wait=True
)
assert event, 'no event for EscrowAccessSecretStoreTemplate.AgreementCreated'

event = keeper.lock_reward_condition.subscribe_condition_fulfilled(
    agreement_id,
    30,
    _log_event(keeper.lock_reward_condition.FULFILLED_EVENT),
    (),
    wait=True
)
assert event, 'no event for LockRewardCondition.Fulfilled'

event = keeper.access_secret_store_condition.subscribe_condition_fulfilled(
    agreement_id,
    30,
    _log_event(keeper.escrow_reward_condition.FULFILLED_EVENT),
    (),
    wait=True
)
assert event, 'no event for AccessSecretStoreCondition.Fulfilled'

event = keeper.escrow_reward_condition.subscribe_condition_fulfilled(
    agreement_id,
    30,
    _log_event(keeper.escrow_reward_condition.FULFILLED_EVENT),
    (),
    wait=True
)
assert event, 'no event for EscrowReward.Fulfilled'
assert ocn.agreements.is_access_granted(agreement_id, ddo.did, consumer_account.address)

ocn.assets.consume(
    agreement_id,
    ddo.did,
    sa.service_definition_id,
    consumer_account,
    "downloads_nile")
logging.info('Success buying asset.')


