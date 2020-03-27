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
import os
from pathlib import Path

# Import mantaray and the Ocean API (squid)
# mantaray_utilities is an extra helper library to simulate interactions with the Ocean API.
import squid_py
from mantaray_utilities.user import create_account
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
from mantaray_utilities import logging as manta_logging, config

# Setup logging to a higher level and not flood the console with debug messages

manta_logging.logger.setLevel('INFO')
logging.info("Squid API version: {}".format(squid_py.__version__))
print("squid-py Ocean API version:", squid_py.__version__)

#%%
# Get the configuration file path for this environment
OCEAN_CONFIG_PATH = Path(os.path.expanduser(os.environ['OCEAN_CONFIG_PATH']))
assert OCEAN_CONFIG_PATH.exists(), "{} - path does not exist".format(OCEAN_CONFIG_PATH)

logging.critical("Configuration file selected: {}".format(OCEAN_CONFIG_PATH))
logging.critical("Deployment type: {}".format(config.get_deployment_type()))
logging.critical("Squid API version: {}".format(squid_py.__version__))

#%%
# Instantiate Ocean with the default configuration file.
configuration = Config(OCEAN_CONFIG_PATH)
squid_py.ConfigProvider.set_config(configuration)
ocn = Ocean(configuration)
logging.critical("Ocean smart contract node connected ".format())
faucet_url = ocn.config.get('keeper-contracts', 'faucet.url')

# %% [markdown]
# ## Section 3: Create new user account and fill with some ether

#%%
selected_account = create_account(faucet_url, wait=True)

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

# %% [markdown]
# ## Requesting tokens
# For development and testing, we have a magical function which will give you free testnet Ocean Token!
#
# Your balance should be increased by 1 - but only after the block has been mined! Try printing your balance
# multiple times until it updates.
# %%
print("Starting Ocean balance: {:0.2f}".format(ocn.accounts.balance(selected_account).ocn/10**18))
success = ocn.accounts.request_tokens(selected_account, 1)
# The result will be true or false
assert success

#%%
# Execute this after some time has passed to see the update!
print("Updated Ocean balance: {:0.2f}".format(ocn.accounts.balance(selected_account).ocn/10**18))

# %% [markdown]
# ## Asynchronous interactions
# Many methods in the API will include a call to
# [.waitForTransactionReceipt(transaction_hash)](https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.waitForTransactionReceiptj),
# which explicitly pauses execution until the transaction has been mined. This will return the Transaction Receipt. When interacting
# with the blockchain, things my take some time to execute!
