# %% [markdown]
# # Pre-sail checklist - Python API for Ocean
# With the Ocean Protocol components running, test the Squid API (Python API).
# Instantiate the API with your selected `config.ini` file, or use the default for this environment.

# %% [markdown]
# ## Import the API, `squid-py`, and a simple utilities library `mantaray_utilities`.
#%%
# Standard imports
import logging
import json
import pip_api
from pathlib import Path
import os

# Import mantaray and the Ocean API (squid)
import squid_py
from squid_py.ocean.ocean import Ocean
from squid_py import ConfigProvider
from squid_py.config import Config
import mantaray_utilities as manta_utils
manta_utils.logging.logger.setLevel('INFO')
from squid_py.keeper.web3_provider import Web3Provider

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
# ## Assert that your contract ABI files match those in the test network
# The following cell performs some sanity checks on versions of smart contracts. The smart contract signatures
# are placed in an 'artifacts' folder. When you pip-install the squid-py API, these artifacts are located in the
# virtual environment, and you don't need to worry about them. For demonstration purposes, I've moved the artifacts
# into the project folder here.

# %%
# Assert versions of contract definitions (ABI files) match your installed keeper-contracts package version.
version_kc_installed = 'v'+str(pip_api.installed_distributions()['keeper-contracts'].version)
network_name = 'nile'
folder_artifacts = configuration.get('keeper-contracts', 'keeper.path')
path_artifacts = Path.cwd() / folder_artifacts
assert path_artifacts.exists()
for path_artifact_file in path_artifacts.glob("*.{}.json".format(network_name)):
    with open(path_artifact_file) as fp:
        artifact_dict = json.load(fp)
    assert artifact_dict['version'] == version_kc_installed, \
        "Artifact version mismatch, ABI files {} != {} specified in environment".format(artifact_dict['version'], version_kc_installed)
logging.info("Contract ABI == installed version {}, confirmed".format(version_kc_installed))

#%%
# Assert code at this smart contract address
from squid_py.keeper.web3_provider import Web3Provider
ConfigProvider.set_config(configuration)
this_web3 = Web3Provider.get_web3()
for path_artifact_file in path_artifacts.glob("*.{}.json".format(network_name)):
    with open(path_artifact_file) as fp:
        artifact_dict = json.load(fp)
    code = this_web3.eth.getCode(artifact_dict['address'])
    assert code, "No code found on-chain for {} at {}".format(path_artifact_file, artifact_dict['address'])
logging.info("All {} ABI addresses confirmed to exist on-chain.".format(artifact_dict['version']))

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