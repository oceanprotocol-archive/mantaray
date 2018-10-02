#%%
"""
Test functionality of squid-py wrapper.
"""

#%% Imports
import pathlib
import squid_py.ocean as ocean
import sys
import random

# %% Logging
import logging

loggers_dict = logging.Logger.manager.loggerDict

logger = logging.getLogger()
logger.handlers = []

# Set level
logger.setLevel(logging.INFO)

# FORMAT = "%(asctime)s - %(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"
# FORMAT = "%(asctime)s %(levelno)s: %(module)30s %(message)s"
FORMAT = "%(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"

DATE_FMT = "%Y-%m-%d %H:%M:%S"
DATE_FMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(FORMAT, DATE_FMT)

# Create handler and assign
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.handlers = [handler]
logger.info("Logging started")

#%% Instantiate the wrapper

# The contract addresses are loaded from file
PATH_CONFIG = pathlib.Path.cwd() / 'config_local.ini'
assert PATH_CONFIG.exists(), "{} does not exist".format(PATH_CONFIG)

ocean = ocean.Ocean(host='http://0.0.0.0', port=8545, config_path=PATH_CONFIG)

logging.info("Ocean smart contract node connected at {}".format(ocean.node_uri))
logging.info("{:>40} {}".format("Token contract address:", ocean.token.address))
logging.info("{:>40} {}".format("Authentication contract atddress:", ocean.auth.address))
logging.info("{:>40} {}".format("Market contract address:", ocean.market.address))

logging.info("Metadata store (provider) located at: {}".format(ocean.metadata.base_url))

#%% Transfer fundsj
# By default, 10 wallet addresses are created in Ganache
# A simple wrapper for each address is created to represent a user
# A few users are instantiated and listed

class User():
    def __init__(self,num,ocean_obj):
        self.name = 'user' + str(num)
        self.ocean = ocean_obj
        self.address = self.ocean.helper.web3.eth.accounts[num]
        self.balance = self.update_balance()

        logging.debug(self)

    def __str__(self):
        self.update_balance()
        return "{} at {}... with {} token".format(self.name,self.address[0:6],self.balance)

    def update_balance(self):
        self.balance = self.ocean.token.get_token_balance(self.address)

    def request_dev_tokens(self,amount):
        """For development, a user can request free tokens"""
        self.ocean.market.request_tokens(amount, self.address)

users = list()
for i in range(len(ocean.helper.web3.eth.accounts)):
    user = User(i,ocean)
    user.request_dev_tokens(random.randint(0,100))
    users.append(user)

#%%
for u in users: print(u)

#%%

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


    # events = get_events(filter_token_published)
    # assert events
    # assert events[0].args['_id'] == request_id
    # on_chain_enc_token = events[0].args["_encryptedAccessToken"]
