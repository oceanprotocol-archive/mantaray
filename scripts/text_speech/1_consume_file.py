import sys

import logging
# loggers_dict = logging.Logger.manager.loggerDict
#
# logger = logging.getLogger()
# logger.handlers = []
#
# # Set level
# logger.setLevel(logging.DEBUG)
#
# # FORMAT = "%(asctime)s - %(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"
# # FORMAT = "%(asctime)s %(levelno)s: %(module)30s %(message)s"
# FORMAT = "%(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"
#
# DATE_FMT = "%Y-%m-%d %H:%M:%S"
# DATE_FMT = "%Y-%m-%d %H:%M:%S"
# formatter = logging.Formatter(FORMAT, DATE_FMT)
#
# # Create handler and assign
# handler = logging.StreamHandler(sys.stderr)
# handler.setFormatter(formatter)
# logger.handlers = [handler]
# logger.debug("Logging started")

#%%
# Standard imports
import os
from pathlib import Path
import json
from time import sleep
# Ocean imports
import squid_py
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
from pprint import pprint
import mantaray_utilities as manta_utils
from mantaray_utilities.blockchain import subscribe_event
from mantaray_utilities.user import password_map

#%% CONFIG

OCEAN_CONFIG_PATH = Path().cwd() / 'config_nile.ini'
assert OCEAN_CONFIG_PATH.exists(), "{} - path does not exist".format(OCEAN_CONFIG_PATH)
os.environ['OCEAN_CONFIG_PATH'] = str(OCEAN_CONFIG_PATH)

PASSWORD_PATH=Path().cwd() / ".nile_passwords"
assert PASSWORD_PATH.exists()
os.environ["PASSWORD_PATH"] = str(PASSWORD_PATH)

MARKET_PLACE_PROVIDER_ADDRESS="0x376817c638d2a04f475a73af37f7b51a2862d567"
os.environ["MARKET_PLACE_PROVIDER_ADDRESS"] = MARKET_PLACE_PROVIDER_ADDRESS

JSON_TEMPLATE = Path().cwd() / 'metadata_template.json'
assert JSON_TEMPLATE.exists()


#%% ARGPARSE
import argparse
parser = argparse.ArgumentParser(description='Videos to images')
parser.add_argument('--did', type=str, help='DID of asset')

args = parser.parse_args()
logging.info("************************************************************".format())
logging.info("*** ETHBERLINZWEI HACKATHON                              ***".format())
logging.info("*** SPEECH2TEXT                                          ***".format())
logging.info("*** STEP 2                                               ***".format())
logging.info("************************************************************".format())

logging.info("".format())
logging.info("Purchasing an audio asset, DID: {}".format(args.did))
logging.info("".format())

#%%
# Get the configuration file path for this environment

logging.info("Configuration file selected: {}".format(OCEAN_CONFIG_PATH))
# logging.critical("Deployment type: {}".format(manta_utils.config.get_deployment_type()))
logging.info("Squid API version: {}".format(squid_py.__version__))

#%%
# Instantiate Ocean with the default configuration file.
configuration = Config(OCEAN_CONFIG_PATH)
squid_py.ConfigProvider.set_config(configuration)
ocn = Ocean(configuration)


#%%
def get_asset_ddo(did):
    asset = ocn.assets.resolve(args.did)
    return asset
    # print("RESOLVE")
    # print(res.did)
    # print(dir(res))
    # print(res.metadata)
    # raise


ddo = get_asset_ddo(args.did)
metadata = ddo.metadata

logging.info("".format())
logging.info("Asset {} resolved".format(args.did))
logging.info("Price {}".format(metadata['base']['price']))

if 'additionalInformation' in metadata.keys():
    logging.info("Reward {}".format(metadata['additionalInformation']['reward']))
    logging.info("Number processors requested {}".format(metadata['additionalInformation']['numberNodes']))

# pprint(metadata)

#%%
# Get a consumer account
consumer_account = manta_utils.user.get_account_by_index(ocn,1)
logging.info("".format())
logging.info("Processor address: {}".format(consumer_account.address))
logging.info("Processor   ETH: {:0.1f}".format(ocn.accounts.balance(consumer_account).eth/10**18))
logging.info("Processor OCEAN: {:0.1f}".format(ocn.accounts.balance(consumer_account).ocn/10**18))
assert ocn.accounts.balance(consumer_account).eth/10**18 > 1, "Insufficient ETH in account {}".format(consumer_account.address)

# Ensure the consumer always has enough Ocean Token (with a margin)
if ocn.accounts.balance(consumer_account).ocn/10**18 < int(metadata['base']['price']) + 1:
    logging.info("Insufficient Ocean Token balance for this asset!".format())
    refill_amount = int(15 - ocn.accounts.balance(consumer_account).ocn/10**18)
    logging.info("Requesting {} tokens".format(refill_amount))
    ocn.accounts.request_tokens(consumer_account, refill_amount)
    logging.info("New OCEAN balance: {:0.1f}".format(ocn.accounts.balance(consumer_account).ocn/10**18))

#%% ORDER
agreement_id = ocn.assets.order(ddo.did, 'Access', consumer_account)
logging.info("Consumer has placed an order for asset {}".format(ddo.did))
logging.info("The service agreement ID is {}".format(agreement_id))

# %%

keeper = squid_py.keeper.Keeper.get_instance()

subscribe_event("created agreement", keeper, agreement_id)
subscribe_event("lock reward", keeper, agreement_id)
subscribe_event("access secret store", keeper, agreement_id)
subscribe_event("escrow reward", keeper, agreement_id)

#%%
assert ocn.agreements.is_access_granted(agreement_id, ddo.did, consumer_account.address)
ocn.assets.consume(agreement_id, ddo.did, 'Access', consumer_account, 'downloads_nile')

logging.info('Success buying asset.')
