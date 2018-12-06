# %% [markdown]
# Run this script to test the Ocean wrapper (squid-py).
# Instantiate the wrapper with your selected `config.ini` file

#%%
# Standard imports
import logging

# Import mantaray and the Ocean API (squid)
from squid_py.ocean.ocean import Ocean
import mantaray_utilities.config as manta_config
import mantaray_utilities.logging as manta_logging

#%%
# Get the configuration file path for this environment
CONFIG_INI_PATH = manta_config.get_config_file_path()
logging.info("Configuration file selected: {}".format(CONFIG_INI_PATH))

#%%
# Instantiate Ocean
ocn = Ocean(CONFIG_INI_PATH)

#%%
print("***OCEAN***")
print("{} accounts".format(len(ocn.accounts)))
for account in ocn.accounts:
    print(account)

# A utility function is provided to summarize the Ocean class
manta_config.print_ocean(ocn)

