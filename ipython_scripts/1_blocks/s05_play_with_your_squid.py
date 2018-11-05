# %%
"""
Test functionality of squid-py wrapper.
"""


# %% Imports
from pathlib import Path
import squid_py.ocean as ocean_wrapper
# from squid_py.utils.web3_helper import convert_to_bytes, convert_to_string, convert_to_text, Web3Helper
import sys
import random
import json
from pprint import pprint
import squid_py.ocean as ocean

# %% Logging
import logging
loggers_dict = logging.Logger.manager.loggerDict
logger = logging.getLogger()
logger.handlers = []
# Set level
logger.setLevel(logging.INFO)
FORMAT = "%(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(FORMAT, DATE_FMT)
# Create handler and assign
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.handlers = [handler]
logger.info("Logging started")

# %% Instantiate the wrapper

# The contract addresses are loaded from file
# CHOOSE YOUR CONFIGURATION METHOD
# PATH_CONFIG = Path.cwd() / 'config_local.ini'
# PATH_CONFIG = Path.cwd() / '..' / '..' / 'config_k8s.ini'
PATH_CONFIG = Path.cwd() / 'config_k8s.ini'
# PATH_CONFIG = Path.cwd() / 'config_local.ini'
assert PATH_CONFIG.exists(), "{} does not exist".format(PATH_CONFIG)

ocn = ocean.Ocean(PATH_CONFIG)
logging.info("Ocean smart contract node connected ".format())

# %% List the users
ocn.accounts


# %% Get funds to users
# By default, 10 wallet addresses are created in Ganache
# A simple wrapper for each address is created to represent a user
# Users are instantiated and listed

class User():
    def __init__(self,num,account_obj):
        self.name = 'user' + str(num)
        self.account = account_obj
        logging.info(self)

    def __str__(self):
        # self.update_balance()
        return "{}  {}".format(self.name,self.account)

users = list()
for i, acct_address in enumerate(ocn.accounts):
    user = User(i, ocn.accounts[acct_address])


    # print(i, acct_address, account_obj.ocean, account_obj.ether)
    # user.request_dev_tokens(random.randint(0,100))
    # user.account.request_tokens(random.randint(0,100)))
    users.append(user)

#%% List the users
users[0].name = 'Data Scientist'
users[1].name = 'Data Owner'
for u in users: print(u)

#%% Get some Ocean token
for usr in users:
    usr.account.request_tokens(random.randint(0,100))

for u in users: print(u)

# %% Register some assets

# The sample asset metadata is stored in a .json file
PATH_ASSET1 = pathlib.Path.cwd() / 'sample_assets' / 'sample1.json'
assert PATH_ASSET1.exists()
with open(PATH_ASSET1) as f:
    dataset = json.load(f)

logging.info("Asset metadata for {}: type={}, price={}".format(dataset['base']['name'],dataset['base']['type'],dataset['base']['price']))

registered_asset = users[0].register_asset(dataset)

asset = ocn.metadata.register_asset(dataset)
assert ocean_provider.metadata.get_asset_ddo(asset['assetId'])['base']['name'] == asset['base']['name']
ocean_provider.metadata.retire_asset(asset['assetId'])

# %% List assets
asset_ddo = ocn.metadata.get_asset_ddo(dataset['assetId'])
assert ocn.metadata.get_asset_ddo(dataset['assetId'])['base']['name'] == dataset['base']['name']
# %%

# import time

# import squid_py.acl as acl
# from squid_py.ocean import Ocean
# from squid_py.utils.web3_helper import convert_to_string

def get_events(event_filter, max_iterations=100, pause_duration=0.1):
    events = event_filter.get_new_entries()
    i = 0
    while not events and i < max_iterations:
        i += 1
        time.sleep(pause_duration)
        events = event_filter.get_new_entries()

    if not events:
        print('no events found in %s events filter.' % str(event_filter))
    return events


def process_enc_token(event):
    # should get accessId and encryptedAccessToken in the event
    print("token published event: %s" % event)


def test_keeper():
    expire_seconds = 9999999999
    asset_price = 100
    ocean = Ocean(host='http://localhost', port=8545, config_path='config_local.ini')
    market = ocean.market
    token = ocean.token
    auth = ocean.auth
    provider_account = ocean.helper.web3.eth.accounts[0]
    consumer_account = ocean.helper.web3.eth.accounts[1]
    assert market.request_tokens(2000, provider_account)
    assert market.request_tokens(2000, consumer_account)

    # 1. Provider register an asset
    asset_id = market.register_asset(json_dict['base']['name'],json_dict['base']['description'], asset_price, provider_account)
    assert market.check_asset(asset_id)
    assert asset_price == market.get_asset_price(asset_id)

    json_dict['assetId'] = ocean.web3.toHex(asset_id)
    ocean.metadata.register_asset(json_dict)
    expiry = int(time.time() + expire_seconds)

    pubprivkey = acl.generate_encryption_keys()
    pubkey = pubprivkey.public_key
    req = auth.concise_contract.initiateAccessRequest(asset_id,
                                                      provider_account,
                                                      pubkey,
                                                      expiry,
                                                      transact={'from': consumer_account})
    receipt = ocean.helper.get_tx_receipt(req)

    send_event = auth.contract.events.AccessConsentRequested().processReceipt(receipt)
    request_id = send_event[0]['args']['_id']

    assert auth.get_order_status(request_id) == 0 or auth.get_order_status(
        request_id) == 1

    # filter_token_published = ocean.helper.watch_event(auth.contract, 'EncryptedTokenPublished', process_enc_token, 0.5,
    #                                                   fromBlock='latest')

    i = 0
    while (auth.get_order_status(request_id) == 1) is False and i < 100:
        i += 1
        time.sleep(0.1)

    assert auth.get_order_status(request_id) == 1

    token.token_approve(ocean.web3.toChecksumAddress(market.address),
                        asset_price,
                        consumer_account)

    buyer_balance_start = token.get_token_balance(consumer_account)
    seller_balance_start = token.get_token_balance(provider_account)
    print('starting buyer balance = ', buyer_balance_start)
    print('starting seller balance = ', seller_balance_start)

    send_payment = market.contract_concise.sendPayment(request_id,
                                                       provider_account,
                                                       asset_price,
                                                       expiry,
                                                       transact={'from': consumer_account, 'gas': 400000})
    receipt = ocean.helper.get_tx_receipt(send_payment)
    print('Receipt: %s' % receipt)

    print('buyer balance = ', token.get_token_balance(consumer_account))
    print('seller balance = ', token.get_token_balance(provider_account))
    ocean.metadata.retire_asset(convert_to_string(asset_id))


#%%
    # events = get_events(filter_token_published)
    # assert events
    # assert events[0].args['_id'] == request_id
    # on_chain_enc_token = events[0].args["_encryptedAccessToken"]




    # def request_dev_tokens(self,amount):
    #     """For development, a user can request free tokens"""
    #     self.ocean.market.request_tokens(amount, self.address)
    #
    # def register_asset(self, dataset):
    #     # Register this asset on the blockchain
    #     asset_id = self.ocean.market.register_asset(dataset['base']['name'], dataset['base']['description'],
    #                                            dataset['base']['price'], self.address)
    #     assert self.ocean.market.check_asset(asset_id)
    #
    #     # logging.info("{} registered".format(asset_id.decode("ascii").rstrip()))
    #     logging.info("registered asset: {}".format(asset_id))
