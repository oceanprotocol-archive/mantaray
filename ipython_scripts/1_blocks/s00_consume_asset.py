# %% [markdown]
# ## Building Blocks: Downloading Datasets
# In this notebook, TODO: description

# %% [markdown]
# ### Section 0: Housekeeping, import modules, and setup logging
#%%
import pathlib
import sys
import logging
from pathlib import Path
import squid_py
from squid_py.ocean.ocean import Ocean

# Add the local utilities package
utilities_path = Path('.') / 'script_fixtures'
if not utilities_path.exists():
    utilities_path = Path('.') / '..' / '..' / 'script_fixtures'
assert utilities_path.exists()

#Get the project root path
PATH_PROJECT_ROOT = utilities_path / '..'
PATH_PROJECT_ROOT.absolute()

utilities_path_str = str(utilities_path.absolute())
if utilities_path_str not in sys.path:
    sys.path.append(utilities_path_str)

import script_fixtures.logging as util_logging
util_logging.logger.setLevel('INFO')

import script_fixtures.user as user
logging.info("Squid API version: {}".format(squid_py.__version__))

# %% [markdown]
# ### Section 1: Instantiate a simulated User
# A 'User' in an abstract class representing a user of Ocean Protocol
#
# Follow Anne Bonny as she purchases an asset which has been registered in Ocean Protocol
#%%
# The contract addresses are loaded from file
PATH_CONFIG = pathlib.Path.cwd() / 'config_local.ini'
assert PATH_CONFIG.exists(), "{} does not exist".format(PATH_CONFIG)

ocn = Ocean(config_file=PATH_CONFIG)
#%%
print("HTTP Client:")
print(ocn._http_client)
print("Secret Store Client:")
print(ocn._secret_store_client)

#%%
# This utility function gets all simulated accounts
users = user.get_all_users(ocn.accounts)

# We don't need this ocn instance reference anymore
del ocn

# Let's take the first unlocked account, and name it the Publisher
consumer1 = [u for u in users if not u.locked][0]
consumer1.name = "Anny Bonny"
consumer1.role = "Consumer"
print(consumer1)

assert consumer1.ocn._http_client.__name__ == 'requests'
assert consumer1.ocn._secret_store_client.__name__ == 'Client'

