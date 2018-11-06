# %% [markdown]

# <p><center>Ocean Protocol</p>
# <p><center>Trilobite pre-release 0.1</center></p>
# <img src="https://oceanprotocol.com/static/media/logo-white.7b65db16.png" alt="drawing" width="200" align="center"/>
# </center>

# %%
# Ocean Protocol
#
# Trilobite release
#
# <img src="https://oceanprotocol.com/static/media/logo-white.7b65db16.png" alt="drawing" width="200"/>
# <img src="https://oceanprotocol.com/static/media/logo.75e257aa.png" alt="drawing" width="200"/>
#
# %% [markdown]
# # Test functionality of squid-py wrapper.

# %% [markdown]
# <img src="https://3c1703fe8d.site.internapcdn.net/newman/gfx/news/hires/2017/mismatchedey.jpg" alt="drawing" width="200" align="center"/>

# %% [markdown]
# ## Section 1: Import modules, and setup logging

# %% [markdown]
# Imports
#%%
from pathlib import Path
import squid_py.ocean as ocean_wrapper
# from squid_py.utils.web3_helper import convert_to_bytes, convert_to_string, convert_to_text, Web3Helper
import sys
import random
import json
from pprint import pprint
import squid_py.ocean as ocean
import names

# %% [markdown]
# Logging
# %%
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
# %% [markdown]
# ## Section 2: Instantiate the Ocean Protocol interface

#%%
# The contract addresses are loaded from file
# CHOOSE YOUR CONFIGURATION HERE
# PATH_CONFIG = Path.cwd() / 'config_local.ini'
PATH_CONFIG = Path.cwd() / '..' / '..' / 'config_k8s.ini'
PATH_CONFIG = Path.cwd() /  'config_local.ini'
# PATH_CONFIG = Path.cwd() / 'config_k8s.ini'
# PATH_CONFIG = Path.cwd() / 'config_local.ini'
assert PATH_CONFIG.exists(), "{} does not exist".format(PATH_CONFIG)

ocn = ocean.Ocean(PATH_CONFIG)
logging.info("Ocean smart contract node connected ".format())


# %% [markdown]
# ## Section 3: Users and accounts
# %% [markdown]
# List the accounts created in Ganache
#%%
ocn.update_accounts()
for address in ocn.accounts:
    print(ocn.accounts[address])

# These accounts have a positive ETH balance
for address, account in ocn.accounts.items():
    assert account.ether >= 0
    assert account.ocean >= 0

# %% [markdown]
# Get funds to users
# By default, 10 wallet addresses are created in Ganache
# A simple wrapper for each address is created to represent a user
# Users are instantiated and listed
#%%
class User():
    def __init__(self, name, role, account_obj):
        self.name = name
        self.role = role
        self.account = account_obj

        logging.info(self)

    def __str__(self):
        try:
            ocean_token = self.account.ocean
        except:
            ocean_token = 0
        return "{:<20} {:<20} {} Ocean token".format(self.name, self.role, ocean_token)

users = list()
for i, acct_address in enumerate(ocn.accounts):
    if i%2 == 0: role = 'Data Scientist'
    else: role = 'Data Owner'
    user = User(names.get_full_name(), role, ocn.accounts[acct_address])
    users.append(user)

#%% [markdown]
# List the users
#%%
for u in users: print(u)

#%% [markdown]
# Get some Ocean token
#%%
for usr in users:
    rcpt = usr.account.request_tokens(random.randint(0,100))
    ocn._web3.eth.waitForTransactionReceipt(rcpt)

for u in users: print(u)

# %% [markdown]
# ## Section 4: Find and publish assets
#%% [markdown]
# List assets

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

