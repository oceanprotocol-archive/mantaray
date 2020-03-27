# %% [markdown]
# ## Building Blocks: Publishing assets
# In this notebook, TODO: description

# %% [markdown]
# ### Section 1: Import modules, and setup logging
#%%
import json
import pathlib
import sys
import logging

import squid_py
from mantaray_utilities.misc import get_ddo_example
from ocean_keeper.utils import get_account
from ocean_utils.agreements.service_factory import ServiceDescriptor
from ocean_utils.agreements.service_types import ServiceTypes
from ocean_utils.ddo.ddo import DDO
from squid_py import Config
from squid_py.ocean.ocean import Ocean
from mantaray_utilities import config

utilities_path = pathlib.Path('.') / 'script_fixtures'
if not utilities_path.exists():
    utilities_path = pathlib.Path('.') / '..' / '..' / 'script_fixtures'
assert utilities_path.exists()

# Get the project root path
PATH_PROJECT_ROOT = utilities_path / '..'
PATH_PROJECT_ROOT.absolute()

utilities_path_str = str(utilities_path.absolute())
if utilities_path_str not in sys.path:
    sys.path.append(utilities_path_str)

logging.info("Squid API version: {}".format(squid_py.__version__))

#%%
# %% [markdown]
# ### Section 2: Instantiate Ocean()
#%%
CONFIG_INI_PATH = config.get_config_file_path()
configuration = Config(CONFIG_INI_PATH)
ocn = Ocean(configuration)

# %% [markdown]
# ### Section 3: register the dataset
#%%
template_id = ocn.keeper.template_manager.create_template_id(
  ocn.keeper.template_manager.SERVICE_TO_TEMPLATE_NAME[ServiceTypes.ASSET_ACCESS]
)

#%%
TEST_DDO = get_ddo_example()

asset = DDO(dictionary=TEST_DDO)
asset_price = 10
attributes = {
    'main': {
        "name": "dataAssetAccessServiceAgreement",
        "creator": "",
        "datePublished": "2019-02-08T08:13:49Z",
        "price": str(asset_price),
        "timeout": 42000
    }
}
service_descriptors = [ServiceDescriptor.access_service_descriptor(asset_price, '/serviceEndpoint', template_id)]
ocn.assets.create(asset.metadata, get_account(0), service_descriptors)
