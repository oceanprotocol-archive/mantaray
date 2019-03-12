# %% [markdown]
# # Pre-sail checklist - Python API for Ocean
# With the Ocean Protocol components running, test the Squid API (Python API).
# Instantiate the API with your selected `config.ini` file, or use the default for this environment.

# %% [markdown]
# ## Import the API, `squid-py`, and a simple utilities library `mantaray_utilities`.
#%%
# Standard imports
import logging

# Import mantaray and the Ocean API (squid)
import squid_py
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
import mantaray_utilities as manta_utils
manta_utils.logging.logger.setLevel('INFO')

print("squid-py Ocean API version:", squid_py.__version__)

# %% [markdown]
# In order to manage the different environments Mantaray runs in, we have a series of environment variables
# which are used in the utilities library to resolve paths and keep behavior consistent. In the JupyterHub
# deployment, all of this is taken care of for you.

#%%
# Get the configuration file path for this environment
logging.critical("Deployment type: {}".format(manta_utils.config.get_deployment_type()))

CONFIG_INI_PATH = manta_utils.config.get_config_file_path()
logging.critical("Configuration file selected: {}".format(CONFIG_INI_PATH))

#%% [markdown]
# ## Connect to Ocean Protocal with the configuration file

#%%
# Load the configuration
configuration = Config(CONFIG_INI_PATH)
print("Configuration loaded. Will connect to a node at: ", configuration.keeper_url)

# %% [markdown]
# Feel free to inspect the `configuration` object.

# %% [markdown]
# From the configuration, instantiate the Ocean object, the primary interface to Ocean Protocol.
# %%
# Instantiate Ocean
ocn = Ocean(configuration)

# %% [markdown]
# The following cell will print some summary information of the Ocean connection.
#TODO: add pretty printing of the connection

#%%
print("***OCEAN***")
print("{} accounts".format(len(ocn.accounts._accounts)))
for i, account in enumerate(ocn.accounts._accounts):
    print(i, account.address)

#%% [markdown]
# ## Alternatively, connect to Ocean with a configuration as dictionary
# The configuration of the client (mantaray) can be inspected in the below code cells. The following configuration
# is set for local testing.

#%%
config_dict = {
    'keeper-contracts': {
        # Point to an Ethereum RPC client. Note that Squid learns the name of the network to work with from this client.
        'keeper.url': 'http://localhost:8545',
        # Specify the keeper contracts artifacts folder (has the smart contracts definitions json files). When you
        # install the package, the artifacts are automatically picked up from the `keeper-contracts` Python
        # dependency unless you are using a local ethereum network.
        'keeper.path': 'artifacts',
        'secret_store.url': 'http://localhost:12001',
        'parity.url': 'http://localhost:8545',
        'parity.address': '',
        'parity.password': '',

    },
    'resources': {
        # aquarius is the metadata store. It stores the assets DDO/DID-document
        'aquarius.url': 'http://localhost:5000',
        # Brizo is the publisher's agent. It serves purchase and requests for both data access and compute services
        'brizo.url': 'http://localhost:8030',
        # points to the local database file used for storing temporary information (for instance, pending service agreements).
        'storage.path': 'squid_py.db',
        # Where to store downloaded asset files
        'downloads.path': 'consume-downloads'
    }
}
# %%
# You may modify the dictionary object and uncomment the next cell to test
#%% [markdown]
# ```
# # Instantiate Ocean from the above dictionary
# configuration = Config(filename=None, options_dict=config_dict)
# ocn = Ocean(configuration)
# print("***OCEAN***")
# print("{} accounts".format(len(ocn.accounts._accounts)))
# for i, account in enumerate(ocn.accounts._accounts):
#     print(i, account.address)
# ```