# %% [markdown]
# ## Building Blocks: Getting tokens to your users
# In this notebook, we will work with a class which represents a
# User of Ocean Protocol.
# To use Ocean, a User requires
# - A wallet address
# - A password
#
# With this information, the Ocean instance can be instantiated with the Ocean.main_account attribute.
# This attribute enables the User to unlock event calls in the networks.
# This class will be used in later scripts to simulate behaviour of actors on the network.
# See the /script_fixtures directory for utilities such as the User() class

# %% [markdown]
# ### Section 0: Import modules, and setup logging

#%%
# When running in IPython, ensure the path is obtained
# This may vary according to your environment
from pathlib import Path
if not 'PATH_PROJECT' in locals():
    PATH_PROJECT = Path.cwd()
print("Project root path:", PATH_PROJECT)
#%%
import sys
import random
import configparser
import names
import logging
import squid_py
from squid_py.ocean.ocean import Ocean

# Add the local utilities package
utilities_path = PATH_PROJECT / 'script_fixtures'
assert utilities_path.exists()
utilities_path = str(utilities_path.absolute())
if utilities_path not in sys.path:
    sys.path.append(utilities_path)

import script_fixtures.logging as util_logging
util_logging.logger.setLevel('INFO')

import script_fixtures.user as user

logging.info("Squid API version: {}".format(squid_py.__version__))

# %% [markdown]
# ## Section 1: Instantiate the Ocean Protocol interface

#%%
# The contract addresses are loaded from file
# CHOOSE YOUR CONFIGURATION HERE
PATH_CONFIG = Path.cwd() / 'config_local.ini'
PATH_CONFIG = Path.cwd() / 'config_k8s_deployed.ini'
assert PATH_CONFIG.exists(), "{} does not exist".format(PATH_CONFIG)

ocn = Ocean(PATH_CONFIG)
logging.info("Ocean smart contract node connected ".format())

ocn.config.keeper_path

# List the accounts created in Ganache
# ocn.accounts is a {address: Account} dict

print("Ocean accounts:")
for address in ocn.accounts:
    acct = ocn.accounts[address]
    print(acct.address)

#%%
# These accounts have a balance of ETH and Ocean Token
for address, account in ocn.accounts.items():
    assert account.balance.eth >= 0
    assert account.balance.ocn >= 0

# %% [markdown]
# From accounts -> Users
#
# A simple wrapper for each address is created to represent a user
# This wrapper is presented below, and later used as a fixture,
# See: ./script_fixtures/user.py

#%%
class User():
    def __init__(self, name, role, address, config_path=None):
        """
        A class to represent a User of Ocean Protocol.
        A User's account can be *locked*. To unlock an account, provide the password to the .unlock() method.

        :param name: Just to keep track and personalize the simulation
        :param role: Also just for personalizing
        :param address: This the account address
        :param config_path: The Ocean() library class *requires* a config file
        """
        self.name = name
        self.address = address
        self.role = role
        self.credentials = False # Does this config file have a user address and pasword?
        self.config_path = config_path

        self.ocn = None
        self.account = None

        # If the account is unlocked, instantiate Ocean and the Account classes
        if self.address.lower() in PASSWORD_MAP:
            password = PASSWORD_MAP[self.address.lower()]

            # The ocean class REQUIRES a .ini file -> need to create this file!
            if not self.config_path:
                self.config_fname = "{}_{}_config.ini".format(self.name,self.role).replace(' ', '_')
                config_path = self.create_config(password) # Create configuration file for this user

            # Instantiate Ocean and Account for this User
            self.ocn = Ocean(config_path)
            if self.ocn.main_account: # If this attribute exists, the password is stored
                self.credentials = True
            # self.unlock(password)
            acct_dict_lower = {k.lower(): v for k, v in ocn.accounts.items()}
            self.account = acct_dict_lower[self.address.lower()]

        logging.info(self)

    def create_config(self, password):
        """Fow now, a new config.ini file must be created and passed into Ocean for instantiation"""
        conf = configparser.ConfigParser()
        assert PATH_CONFIG.exists()
        conf.read(str(PATH_CONFIG))
        conf['keeper-contracts']['parity.address'] = self.address
        conf['keeper-contracts']['parity.password'] = password
        out_path = Path.cwd() / 'user_configurations' / self.config_fname
        logging.info("Create a new configuration file for {}.".format(self.name))
        with open(out_path, 'w') as fp:
            conf.write(fp)
        return out_path

    def __str__(self):
        if not self.credentials:
            return "{:<20} {:<20} LOCKED ACCOUNT".format(self.name, self.role)
        else:
            ocean_token = self.account.ocean_balance
            return "{:<20} {:<20} with {} Ocean token".format(self.name, self.role, ocean_token)

    def __repr__(self):
        return self.__str__()

#%% [markdown]
# Users are instantiated and listed
#%%
# Selected accounts are unlocked via password
PASSWORD_MAP = {
    '0x00bd138abd70e2f00903268f3db08f2d25677c9e' : 'node0',
    '0x068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0' : 'secret',
    '0xa99d43d86a0758d5632313b8fa3972b6088a21bb' : 'secret',
    '0x64137aF0104d2c96C44bb04AC06f09eC84CC5Ae4' : 'test',
}

# Create some simulated users of Ocean Protocol
# Alternate between Data Scientists (Consumers)
# and Data Owners (providers)
users = list()
for i, acct_address in enumerate(ocn.accounts):
    if i%2 == 0: role = 'Data Scientist'
    else: role = 'Data Owner'
    user = user.User(names.get_full_name(), role, acct_address)
    users.append(user)

# Select only unlocked accounts
unlocked_users = [u for u in users if u.credentials]
logging.info("Selected {} unlocked accounts for simulation.".format(len(unlocked_users)))

#%%
# (Optional)
# Delete the configuration files in the /user_configurations folder
for f in Path('.').glob('user_configurations/*.ini'):
    f.unlink()

#%% [markdown]
# List the users
#%%
for u in unlocked_users: print(u)

#%% [markdown]
# Get some Ocean token
#%%
for usr in unlocked_users:
    if usr.account.ocean_balance == 0:
        rcpt = usr.account.request_tokens(random.randint(0,100))
        usr.ocn._web3.eth.waitForTransactionReceipt(rcpt)

#%% [markdown]
# List the users, and notice the updated balance
#%%
for u in unlocked_users: print(u)