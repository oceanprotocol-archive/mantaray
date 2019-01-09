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
import mantaray_utilities.config as manta_config
import mantaray_utilities.logging as manta_logging
import mantaray_utilities.asset_pretty_print as manta_print
# %% For testing, set the desired environment
# os.environ['USE_K8S_CLUSTER'] = 'true'

#%%
# Get the configuration file path for this environment
logging.critical("Deployment type: {}".format(manta_config.get_deployment_type()))
CONFIG_INI_PATH = manta_config.get_config_file_path()
logging.critical("Configuration file selected: {}".format(CONFIG_INI_PATH))

#%% [markdown]
# ## Connect to Ocean with a configuration file
# The following cell is very verbose, since logging is set at lowest level for demo/debugging. In later notebooks, the debug logs are hidden using `manta_logging`.

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
manta_print.print_ocean(ocn)

#%% [markdown]
# ## Connect to Ocean with a configuration dictionary
# Instantiate Ocean
configuration = Config(CONFIG_INI_PATH)
ocn = Ocean(configuration)
