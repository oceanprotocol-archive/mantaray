# %% [markdown]
# # Getting Underway - wallets, passwords and tokens
#
# To interact in Ocean Protocol, you will need a wallet and you will fund it with some
# Token to access the assets in the network.
#
# In this notebook, we will work with a class which *represents* a
# User of Ocean Protocol.
#
# To use Ocean, a User requires
# - A user account address
# - A password
#
# With this information, the Ocean instance can be instantiated with the Ocean.main_account attribute.
# This attribute enables the User to unlock event calls in the networks.
# This class will be used in later scripts to simulate behaviour of actors on the network.
# See the /script_fixtures directory for utilities such as the User() class

# %% [markdown]
# ### Section 0: Import modules, and setup logging
#%%
# Standard imports
import random
import logging
from pathlib import Path
import csv
# Import mantaray and the Ocean API (squid)
# mantaray_utilities is an extra helper library to simulate interactions with the Ocean API.
import squid_py
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
import mantaray_utilities as manta_utils
logging.info("Squid API version: {}".format(squid_py.__version__))
from pprint import pprint
# Setup logging to a higher level and not flood the console with debug messages
manta_utils.logging.logger.setLevel('CRITICAL')
from squid_py.keeper.web3_provider import Web3Provider

#%%
# Get the configuration file path for this environment
# You can specify your own configuration file at any time, and pass it to the Ocean class.
# os.environ['USE_K8S_CLUSTER'] = 'true'
logging.critical("Deployment type: {}".format(manta_utils.config.get_deployment_type()))
CONFIG_INI_PATH = manta_utils.config.get_config_file_path()
logging.critical("Configuration file selected: {}".format(CONFIG_INI_PATH))

# %% [markdown]
# ## Section 1: Examine the configuration object
#%%
# The API can be configured with a file or a dictionary.
# In this case, we will instantiate from file, which you may also inspect.
# The configuration is a standard library [configparser.ConfigParser()](https://docs.python.org/3/library/configparser.html) object.
print("Configuration file:", CONFIG_INI_PATH)
configuration = Config(CONFIG_INI_PATH)
pprint(configuration._sections)

# %% [markdown]
# Let's look at the 2 parameters that define your identity
# The 20-byte 'parity.address' defines your account address
# 'parity.password' is used to decrypt your private key and securely sign transactions
#%%
print("Currently selected address:",configuration['keeper-contracts']['parity.address'])
print("Associated password:",configuration['keeper-contracts']['parity.password'])

# %% [markdown]
# ## Section 2: Instantiate the Ocean API class with this configuration
# %%
ocn_user1 = Ocean(configuration)
logging.critical("Ocean smart contract node connected ".format())

print(len(ocn_user1.accounts), "accounts exist")
# The Ocean API, during development, queries the blockchain to return all created (simulated) accounts;
for acct in ocn_user1.accounts:
    print(acct)

# Alternatively, the accounts are available on the keeper instance;
# print(ocn.keeper.accounts)
# %% [markdown]
# ### The User Account creed
# *this is my account. there are many like it, but this one is mine.
# my account is my best friend. it is my life. i must master it as i must master my life.
# without me, my account is useless. without my account, i am useless. i must use my account true. *
#
# The Ocean API has a 'main_account', this is the currently active (your) account.
#
# It is not secure to send your password over an unsecured HTTP connection, this is for demonstration only!
#%%
print("Account address: ", ocn_user1.main_account.address)
print("Account password: ", ocn_user1.main_account.password)
print("Account Ether balance: ", ocn_user1.main_account.ether_balance) # TODO: Convert from wei?
print("Account Ocean Token balance: ", ocn_user1.main_account.ocean_balance)

flag_unlocked = Web3Provider.get_web3().personal.unlockAccount(ocn_user1.main_account.address, ocn_user1.main_account.password)
print("Account unlocked:", flag_unlocked)
# The following method can be used to lock an account
#Web3Provider.get_web3().personal.lockAccount(ocn.main_account.address)
