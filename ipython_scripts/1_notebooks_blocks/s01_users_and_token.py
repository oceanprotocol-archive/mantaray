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

import logging
from pathlib import Path
import os
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
manta_utils.logging.logger.setLevel('INFO')
from squid_py.keeper.web3_provider import Web3Provider
# os.environ['USE_K8S_CLUSTER'] = 'True' # Enable this for testing local -> AWS setup
# %%
# Get all passwords
# TODO: Move to utils
import csv
passwords = dict()
path_passwords = manta_utils.config.get_project_path() / 'passwords.csv'
with open(path_passwords) as f:
    for row in csv.reader(f):
        if row:
            passwords[row[0]] = row[1]

passwords = {k.lower(): v for k, v in passwords.items()}

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
user1_address = configuration['keeper-contracts']['parity.address']
user1_pass = configuration['keeper-contracts']['parity.password']
print("Currently selected address:", user1_address)
print("Associated password:", user1_pass)

# %% [markdown]
# ## Section 2: Instantiate the Ocean API class with this configuration
# The Ocean API has an attribute listing all created (simulated) accounts in your local node
# %%
ocn = Ocean(configuration)
logging.critical("Ocean smart contract node connected ".format())

# %% [markdown]
# An account has a balance of Ocean Token, Ethereum, and requires a password to sign any transactions
# %%
# List the accounts in the network
print(len(ocn.accounts.list()), "accounts exist")
print("{:<5} {:<45} {:<20} {:<12} {}".format("","Address", "Ocean Token Balance", "Password?", "ETH balance"))
for i, acct in enumerate(ocn.accounts.list()):
    acct_balance = ocn.accounts.balance(acct)

    # Check the password
    if acct.password:
        flg_password_exists = True
    elif str.lower(acct.address) in passwords:
        acct.password = passwords[str.lower(acct.address)]
        flg_password_exists = True
    else:
        flg_password_exists = False
    print("{:<5} {:<45} {:<20} {:<12} {}".format(i,acct.address, acct_balance.ocn, flg_pass, acct_balance.eth))
    
# %% [markdown]
# ### The User Account creed
# *this is my account. there are many like it, but this one is mine.
# my account is my best friend. it is my life. i must master it as i must master my life.
# without me, my account is useless. without my account, i am useless. i must use my account true.*
#
# %%
# ### It is not secure to send your password over an unsecured HTTP connection, this is for demonstration only!
#

# One of these existing accounts will be selected as your **current active account**. A simple utility class `Account`, is used to
# hold your address and password, and access your balance in Ether and Ocean Token.
# %%
# Select the account specified in your configuration file as the 'parity.address'
my_acct = [ocn.accounts[addr] for addr in ocn.accounts if addr.lower() == user1_address.lower()][0]
my_acct.password = user1_pass
print("Account Ether balance: ", my_acct.ether_balance) # TODO: Convert from wei?
print("Account Ocean Token balance: ", my_acct.ocean_balance)

# %% [markdown]
# Most of your interaction with the blockchain will require your Password.
#
# %% [markdown]
# ## Requesting tokens
# For development and testing, we have a magical function which will give you free Ocean Token!
#
# The result is a *transaction_hash*. This is your ticket to your *transaction receipt*, or in other words,
# your proof that a transaction was completed (or not!).
#
# Your balance should be increased by 1 - but only after the block has been mined! Try printing your balance
# multiple times until it updates.
# %%
my_acct.request_tokens(1)
# %%
# This will update after the transaction has been mined!
print("Account Ocean Token balance: ", my_acct.ocean_balance)

# %% [markdown]
# ## Asynchronous interactions
# Generally, many methods in the API will include a call to
# [.waitForTransactionReceipt(transaction_hash)](https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.waitForTransactionReceiptj),
# which explicitly pauses execution until the transaction has been mined. This will return the Transaction Receipt.
# %%
#TODO: This is refactored in latest to .request_tokens_wait()!
tx_hash = my_acct.request_tokens(1)
Web3Provider.get_web3().eth.waitForTransactionReceipt(tx_hash)

# %% [markdown]
# ## Uncomment below to fund all accounts, make it rain!
# %%
# Quickly fund all accounts
# Request token for all accounts
# for acct_address in ocn.accounts:
#     this_acct = ocn.accounts[acct_address]
#     if this_acct.password:
#         this_acct.request_tokens(100)

