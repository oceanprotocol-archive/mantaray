# %% [markdown]
# ## Building Blocks: Searching and listing registered assets
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
import requests
import json
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

import script_fixtures.asset_pretty_print as util_pprint

logging.info("Squid API version: {}".format(squid_py.__version__))

# %% [markdown]
# ### Section 1: Assets in the MetaData store (Aquarius)
# Anyone can search assets in the public metadata stores
#%%
# The contract addresses are loaded from file
PATH_CONFIG = pathlib.Path.cwd() / 'config_local.ini'
assert PATH_CONFIG.exists(), "{} does not exist".format(PATH_CONFIG)

ocn = Ocean(config_file=PATH_CONFIG)

#%% [markdown]
# The Metadata store is a database wrapped with a REST API
# For all the functionality, see the Swagger documentation
#%%

print("REST API base URL:",ocn.metadata_store._base_url)
print("Swagger API documentation: {}{}".format(ocn.metadata_store._base_url,"/docs/"))

# %% [markdown]
# All stored assets can be listed. This is typically not done in production, as the list would be too large.
# For demonstration purposes, we can access the REST API directly, first retrieve their ID string;
#%%
result = requests.get(ocn.metadata_store._base_url).content
all_ids = json.loads(result)['ids']
for i, id in enumerate(all_ids):
    print(i, id)


# %% [markdown]
# Then, the assets can be retrieved;
#%%
# TODO: Fix
ocn.get_asset('did:ocn:0x93db076c9cfa42f290d4e7d1e0b34271e0e67d6484004a0888b6eac6775213af')

this_asset_endpoint = ocn.metadata_store._base_url  + '/' + id
this_asset_endpoint = ocn.metadata_store._base_url  + '/' + '0x93db076c9cfa42f290d4e7d1e0b34271e0e67d6484004a0888b6eac6775213af'
result = requests.get(this_asset_endpoint).content

# %% [markdown]
# These assets can also be searched, the Asset class is returned from a search
#%% A full text search is implemented
sample_meta_data = squid_py.ddo.metadata.Metadata.get_example()
ocn.search_assets('Random Text')
ocn.search_assets('')
ocn.search_assets('asdfasdfasdf')
ocn.search_assets('Hello do not give me csv')
ocn.search_assets('Ocean')
ocn.search_assets('id')
ocn.search_assets('compression')
ocn.search_assets('contenttype = csv')



for asset in ocn.search_assets('Ocean'):
    print("\nASSET FOUND:", asset)
    print('Asset:')
    util_pprint.print_asset(asset)
    print('DDO:')
    util_pprint.print_ddo(asset.ddo)



# %% [markdown]
# Finally, assets can be deleted from the store

retire_asset_metadata
