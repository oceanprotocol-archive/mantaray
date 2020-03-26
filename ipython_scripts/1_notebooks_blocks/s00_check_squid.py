# %% [markdown]
# # Pre-sail checklist - Python API for Ocean
# With the Ocean Protocol components running, test the Squid API (Python API).
# Instantiate the API with your selected `config.ini` file, or use the default for this environment.

# %% [markdown]
# ## Import the API, `squid-py`, and a simple utilities library `mantaray_utilities`.
#%%
# Standard imports
import logging
import pip_api
from pathlib import Path
import os

# Import mantaray and the Ocean API (squid)
import squid_py
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config

from mantaray_utilities import logging as manta_logging, assert_contracts

manta_logging.logger.setLevel('INFO')

print("squid-py Ocean API version:", squid_py.__version__)

# %% [markdown]
# In order to manage the different environments Mantaray runs in, we have a series of environment variables
# which are used in the utilities library to resolve paths and keep behavior consistent. In the JupyterHub
# deployment, all of this is taken care of for you.

#%%
# Get the configuration file path for this environment
OCEAN_CONFIG_PATH = Path(os.environ['OCEAN_CONFIG_PATH'])
assert OCEAN_CONFIG_PATH.exists(), "{} - path does not exist".format(OCEAN_CONFIG_PATH)
logging.info("OCEAN_CONFIG_PATH:{}".format(OCEAN_CONFIG_PATH))

#%% [markdown]
# ## Connect to Ocean Protocol with the configuration file

#%%
# Load the configuration
configuration = Config(OCEAN_CONFIG_PATH)
print("Configuration loaded. Will connect to a node at: ", configuration.keeper_url)
squid_py.ConfigProvider.set_config(configuration)

# %% [markdown]
# Feel free to inspect the `configuration` object.

# %% [markdown]
# From the configuration, instantiate the Ocean object, the interface to Ocean Protocol.
# %%
# Instantiate Ocean
ocn = Ocean(configuration)

# %% [markdown]
# ## Assert that your contract ABI files match those in the test network
# The following cell performs some sanity checks on versions of smart contracts. The smart contract signatures
# are placed in an 'artifacts' folder. When you pip-install the squid-py API, these artifacts are located in the
# virtual environment, and you don't need to worry about them. For demonstration purposes, I've moved the artifacts
# into the project folder here.

assert_contracts.assert_contract_ABI_versions(ocn, 'nile')
assert_contracts.assert_contract_code(ocn, 'nile')

# %% [markdown]
# The following cell will print some summary information of the Ocean connection.

#%%
print("***OCEAN***")
print("{} accounts".format(len(ocn.accounts.list())))
for i, account in enumerate(ocn.accounts.list()):
    print(i, account.address)

#%% [markdown]
# ## Alternatively, connect to Ocean with a configuration as dictionary
