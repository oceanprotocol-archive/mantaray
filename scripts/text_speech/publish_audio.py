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
parser = argparse.ArgumentParser(description='Publish audio')
parser.add_argument('--url', type=str, help='URL for input audio file')
parser.add_argument('--price', type=int, help='Selling price in Ocean token')
parser.add_argument('--reward', type=int, help='Reward offered in Ocean token')

args = parser.parse_args()
logging.info("************************************************************".format())
logging.info("*** ETHBERLINZWEI HACKATHON                              ***".format())
logging.info("*** SPEECH2TEXT                                          ***".format())
logging.info("*** STEP 1 - CLIENT REGISTERS A CLIP INTO OCEAN PROTOCOL ***".format())
logging.info("************************************************************".format())

logging.info("".format())
logging.info("(Step 1.1 not implemented - upload audio file from client to storage)".format())
logging.info("Publishing Audio to NILE network: {}".format(args.url))
logging.info("Will set price to {} OCEAN".format(args.price))
logging.info("Offering {} OCEAN reward".format(args.reward))
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
# Get a publisher account

publisher_acct = manta_utils.user.get_account_by_index(ocn,0)

#%%
logging.info("Publisher account address: {}".format(publisher_acct.address))
logging.info("Publisher account Testnet 'ETH' balance: {:>6.1f}".format(ocn.accounts.balance(publisher_acct).eth/10**18))
logging.info("Publisher account Testnet Ocean balance: {:>6.1f}".format(ocn.accounts.balance(publisher_acct).ocn/10**18))


def publish(url, price, reward):
    # metadata = squid_py.ddo.metadata.Metadata.get_example()
    # print('Name of asset:', metadata['base']['name'])
    with open(JSON_TEMPLATE, 'r') as f:
        metadata = json.load(f)

    metadata['base']['files'][0]['url'] = url
    metadata['base']['price'] = str(price)
    metadata['additionalInformation']['reward'] = str(reward)
    ddo = ocn.assets.create(metadata, publisher_acct)
    registered_did = ddo.did
    logging.info("New asset registered at {}".format(str(registered_did)))
    logging.info("Asset name: {}".format(metadata['base']['name']))
    logging.info("Encrypted files to secret store, cipher text: [{}...] . ".format(ddo.metadata['base']['encryptedFiles'][:50]))
    return registered_did


registered_did = publish(args.url, args.price, args.reward)

#TODO: Better handling based on reciept
print("Wait for the transaction to complete!")
sleep(10)
# %%
ddo = ocn.assets.resolve(registered_did)
# print("Asset '{}' resolved from Aquarius metadata storage: {}".format(ddo.did,ddo.metadata['base']['name']))

# %% [markdown]
# Similarly, we can verify that this asset is registered into the blockchain, and that you are the owner.

# %%
# We need the pure ID string as in the DID registry (a DID without the prefixes)
asset_id = squid_py.did.did_to_id(registered_did)
owner = ocn._keeper.did_registry.contract_concise.getDIDOwner(asset_id)
# print("Asset ID", asset_id, "owned by", owner)
assert str.lower(owner) == str.lower(publisher_acct.address)
logging.info("".format())
logging.info("Successfully registered Audio!".format())
logging.info("Asset Owner: {}".format(owner))
logging.info("Asset DID: {}".format(registered_did))







