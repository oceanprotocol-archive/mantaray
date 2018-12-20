# %% [markdown]
#

#%%
# Standard imports
import logging
import os
# Import mantaray and the Ocean API (squid)
from squid_py.ocean.ocean import Ocean
import mantaray_utilities.config as manta_config
import mantaray_utilities.logging as manta_logging
import mantaray_utilities.asset_pretty_print as manta_print
# %% For testing, set the desired environment
os.environ['USE_K8S_CLUSTER'] = 'true'

#%%
# Get the configuration file path for this environment
CONFIG_INI_PATH = manta_config.get_config_file_path()
logging.info("Configuration file selected: {}".format(CONFIG_INI_PATH))

#%%
# Instantiate Ocean
ocn = Ocean(CONFIG_INI_PATH)

#%%

