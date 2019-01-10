# %% [markdown]
# # Pre-sail checklist - Python API for Ocean
# With the Ocean Protocol components running, test the Squid API (Python API).
# Instantiate the wrapper with your selected `config.ini` file, or use the default for this environment.

#%%
# Standard imports
import logging
import os
# Import mantaray and the Ocean API (squid)
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
import mantaray_utilities as manta_utils
manta_utils.logging.logger.setLevel('CRITICAL')
# %% For testing, set the desired environment
# os.environ['USE_K8S_CLUSTER'] = 'true'

#%%
# Get the configuration file path for this environment
logging.critical("Deployment type: {}".format(manta_utils.config.get_deployment_type()))
CONFIG_INI_PATH = manta_utils.config.get_config_file_path()
logging.critical("Configuration file selected: {}".format(CONFIG_INI_PATH))

#%% [markdown]
# ## Connect to Ocean with a configuration file

#%%
# Instantiate Ocean
configuration = Config(CONFIG_INI_PATH)
ocn = Ocean(configuration)

#%%
print("***OCEAN***")
print("{} accounts".format(len(ocn.accounts)))
for account in ocn.accounts:
    print(account)

# A utility function is provided to summarize the Ocean class
manta_utils.asset_pretty_print.print_ocean(ocn)

#%% [markdown]
# ## Alternatively, connect to Ocean with a configuration dictionary

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

# Instantiate Ocean
configuration = Config(filename=None, options_dict=config_dict)
ocn = Ocean(configuration)
