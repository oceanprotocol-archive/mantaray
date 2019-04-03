# %% [markdown]
# # Getting Underway - wallets, passwords and tokens
#
# To interact in Ocean Protocol, you will need an account, which you will fund with Token to access the assets
# in the network.
#
# In this notebook, we will demonstrate this behaviour with pre-loaded accounts.
#
# To use Ocean, a User requires
# - A user account address
# - A password
# - Ocean Token

# %% [markdown]
# ### Section 0: Import modules, and setup logging
#%%
# Standard imports
import logging
import random
from pprint import pprint

# Import mantaray and the Ocean API (squid)
# mantaray_utilities is an extra helper library to simulate interactions with the Ocean API.
import squid_py
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
import mantaray_utilities as manta_utils
# Setup logging to a higher level and not flood the console with debug messages
manta_utils.logging.logger.setLevel('INFO')
logging.info("Squid API version: {}".format(squid_py.__version__))
print("squid-py Ocean API version:", squid_py.__version__)

#%% DEBUG
from pathlib import Path
import os
os.environ["USE_K8S_CLUSTER"] = "true"

os.environ["PASSWORD_PATH"] = ".nile_passwords"
path_pass = Path.cwd() / os.environ["PASSWORD_PATH"]
assert path_pass.exists()

os.environ["ADDRESSES_PATH"] = "mantaray_accounts.txt"
path_addresses = Path.cwd() / os.environ["ADDRESSES_PATH"]
assert path_addresses.exists()

#%%
# Get the configuration file path for this environment
# You can specify your own configuration file at any time, and pass it to the Ocean class.
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
# ## Section 2: Instantiate the Ocean API class with this configuration
# The Ocean API has an attribute listing all created (simulated) accounts in your local node
# %%
ocn = Ocean(configuration)
logging.critical("Ocean smart contract node connected ".format())

# %% [markdown]
# ## Section 3: A 'borrowed' user account
# For the purposes of these tutorials, we will borrow one of the accounts to play with the test network. A simple
# wrapper utility will return an account:

#%%
selected_account = manta_utils.user.get_account(ocn)
print("Selected account address:", selected_account.address)

# %% [markdown]
# An account has a balance of Ocean Token, Ethereum, and requires a password to sign any transactions. Similar to
# Ethereum, Ocean Tokens are divisible into the smallest unit of 10^18 of 1 token. There are several accounts
# in the test network as listed below:

# %%
# List the accounts in the network
print(len(ocn.accounts.list()), "accounts exist")
print("Listing first 10 accounts")

# Print a simple table listing the first 10 accounts and balances
print("{:<5} {:<45} {:<20}  {}".format("","Address", "Ocean Token Balance", "ETH balance"))
for i, acct in enumerate(ocn.accounts.list()):
    acct_balance = ocn.accounts.balance(acct)
    print("{:<5} {:<45} {:<20.0f}  {:0.0f}".format(i,acct.address, acct_balance.ocn/10**18, acct_balance.eth/10**18))
    if i == 9: break

# %% [markdown]
# ### It is never secure to send your password over an unsecured HTTP connection, this is for demonstration only!
# ### In a real application, you should always hold your private key locally, secure in a wallet, or use MetaMask
#
# See our documentation page for setting up your Ethereum accounts!
#

# %% [markdown]
# ## Requesting tokens
# For development and testing, we have a magical function which will give you free testnet Ocean Token!
#
# Your balance should be increased by 1 - but only after the block has been mined! Try printing your balance
# multiple times until it updates.
# %%
print("Starting Ocean balance: {:0.2f}".format(ocn.accounts.balance(main_account).ocn/10**18))
success = ocn.accounts.request_tokens(main_account, 1)
# The result will be true or false
assert success

#%%
# Execute this after some time has passed to see the update!
print("Updated Ocean balance: {:0.2f}".format(ocn.accounts.balance(main_account).ocn/10**18))

# %% [markdown]
# ## Asynchronous interactions
# Many methods in the API will include a call to
# [.waitForTransactionReceipt(transaction_hash)](https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.waitForTransactionReceiptj),
# which explicitly pauses execution until the transaction has been mined. This will return the Transaction Receipt. When interacting
# with the blockchain, things my take some time to execute!
