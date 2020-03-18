# %% [markdown]
# # Getting Underway - Publishing asset with private data and compute service
# In this notebook, we will explore how to publish an Asset with private dataset and compute service.
# The private data files will not leave outside the private premises. Instead, a compute service will be
# available for running algorithms to train on the dataset.
#
# A publisher will require access to two services;
# 1. A service to store the MetaData of the asset (part of the DDO) - 'Aquarius'
# 1. A service to manage permissioned access to the compute resource
#    that is allowed to access the private data - 'Brizo'
#
# The publishing of an asset consists of;
# 1. Preparing the asset files locally
# 1. Preparing the metadata of the asset
# 1. Make files URLs or identifiers that can be used to identify the data files when running compute jobs
# 1. Define the attributes of the compute service (i.e. compute resources and service endpoint)
# 1. Registering the metadata and service endpoints into Aquarius
# 1. Registering the asset into the Blockchain (into the DID Registry)

# %% [markdown]
# <p><img src="https://raw.githubusercontent.com/oceanprotocol/mantaray/develop/doc/img/jupyter_cell.png" alt="drawing" width="400" align="center"/></p>
# <p><b>Overall client and service architecture</b></p>

# %% [markdown]
# ### Section 0: Import modules, connect the Ocean Protocol API

#%%
# Standard imports
import json
import logging
import os
from pathlib import Path
# Import mantaray and the Ocean API (squid)
import squid_py
from ocean_keeper.utils import get_account
from ocean_utils.agreements.service_factory import ServiceDescriptor
from ocean_utils.agreements.service_types import ServiceTypes
from ocean_utils.did import did_to_id
from ocean_utils.utils.utilities import get_timestamp
from squid_py.models.algorithm_metadata import AlgorithmMetadata
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
import mantaray_utilities as manta_utils
# from mantaray_utilities.user import password_map

from pprint import pprint
# Setup logging
manta_utils.logging.logger.setLevel('INFO')
from time import sleep
print("squid-py Ocean API version:", squid_py.__version__)

#%%
# Get the configuration file path for this environment
OCEAN_CONFIG_PATH = Path(os.environ['OCEAN_CONFIG_PATH'])
assert OCEAN_CONFIG_PATH.exists(), "{} - path does not exist".format(OCEAN_CONFIG_PATH)

logging.critical("Configuration file selected: {}".format(OCEAN_CONFIG_PATH))
logging.critical("Deployment type: {}".format(manta_utils.config.get_deployment_type()))
logging.critical("Squid API version: {}".format(squid_py.__version__))

#%%
# Instantiate Ocean with the default configuration file.
configuration = Config(OCEAN_CONFIG_PATH)
squid_py.ConfigProvider.set_config(configuration)
ocn = Ocean(configuration)

# %% [markdown]
# ### Section 1: A publisher account in Ocean

#%%
# Get a publisher account

publisher_acct = get_account(0)

#%%
print("Publisher account address: {}".format(publisher_acct.address))
print("Publisher account Testnet 'ETH' balance: {:>6.1f}".format(ocn.accounts.balance(publisher_acct).eth/10**18))
print("Publisher account Testnet Ocean balance: {:>6.1f}".format(ocn.accounts.balance(publisher_acct).ocn/10**18))

# %% [markdown]
# Your account will need some Ocean Token to make real transactions, let's ensure that you are funded!

# %%
# ensure Ocean token balance
# if ocn.accounts.balance(publisher_acct).ocn == 0:
#     ocn.accounts.request_tokens(publisher_acct, 100)

#%% [markdown]
# ### Section 2: Create the Metadata for your asset
# The metadata is a key-value set of attributes which describe your asset
#
# A more complex use case is to manually generate your metadata conforming to Ocean standard, but for demonstration purposes,
# a utility in squid-py is used to generate a sample Meta Data dictionary.

#%%
# Get example of Meta Data from file
metadata_path = 'assets/sample_metadata.json'
with open(metadata_path, 'w') as f:
    metadata = json.load(f)

print('Name of asset:', metadata['main']['name'])
# Print the entire (JSON) dictionary
pprint(metadata)

# %% [markdown]
# Note that the price is included in the Metadata! This will be purchase price you are placing on the asset. You can
# Alter the metadata object at any time before publishing.
#%%
print("Price of Asset:", metadata['main']['price'])
metadata['main']['price'] = "9"  # Note that price is a string
print("Updated price of Asset:", metadata['main']['price'])

#%% [markdown]
# Let's inspect another important component of your metadata - the actual asset files. The files of an asset are
# described by valid URL's. You are responsible for ensuring the URL's are alive. Files may have additional
# information, including a checksum, length, content type, etc.

#%%
for i, file in enumerate(metadata['main']['files']):
    print("Asset link {}: {}".format(i, file['url']))

#%%
# Build compute service to be included in the asset DDO.
cluster = ocn.compute.build_cluster_attributes('kubernetes', '/cluster/url')
containers = [ocn.compute.build_container_attributes(
    "tensorflow/tensorflow",
    "latest",
    "sha256:cb57ecfa6ebbefd8ffc7f75c0f00e57a7fa739578a429b6f72a0df19315deadc")
]
servers = [ocn.compute.build_server_attributes('1', 'xlsize', 16, 0, '16gb', '1tb', 2242244)]
provider_attributes = ocn.compute.build_service_provider_attributes(
    'Azure', 'Compute power 1', cluster, containers, servers
)
attributes = ocn.compute.create_compute_service_attributes(
    13, 3600, publisher_acct.address, get_timestamp(), provider_attributes)

service_endpoint = 'http://localhost:8030/api/v1/brizo/services/compute'
template_id = ocn.keeper.template_manager.create_template_id(
    ocn.keeper.template_manager.SERVICE_TO_TEMPLATE_NAME['compute']
)
service_descriptor = ServiceDescriptor.compute_service_descriptor(attributes, service_endpoint, template_id)

# %% [markdown]
# ## Section 3 Publish the asset
# With this metadata object prepared, we are ready to publish the asset into Ocean Protocol.
#
# The result will be an ID string (DID) registered into the smart contract, and a DID Document stored in Aquarius.
# The asset URLS's are encrypted upon publishing.

# %%
ddo = ocn.assets.create(metadata, publisher_acct)
registered_did = ddo.did
print("New asset registered at", registered_did)

# %% [markdown]
# Inspect the new DDO. We can retrieve the DDO as a dictionary object, feel free to explore the DDO in the cell below!
#%%
ddo_dict = ddo.as_dictionary()
print("DID:", ddo.did)
print("Services within this DDO:")
for svc in ddo_dict['service']:
    print(svc['type'], svc['serviceEndpoint'])

# %% [markdown]
# Note that the 'files' attribute has been modified - all URL's are now removed, and a new 'encryptedFiles'
# attribute is created to store the actual URLs.
#%%
for file_attrib in ddo.metadata['main']['files']:
    assert 'url' not in file_attrib
print("Encrypted files decrypt on purchase! Cipher text: [{}...] . ".format(ddo.metadata['main']['encryptedFiles'][:50]))

# %% [markdown]
# ## Section 4: Verify your asset
# Now, let's verify that this asset exists in the MetaData storage.
#
# A call to assets.resolve() will call the Aquarius service and retrieve the DID Document
#%% {HELLO:test}
#+attr_jupyter: some cell metadata stuff
#+attr_jupyter: some other metadata stuff

# %% [markdown]
# Let's take a look at the compute service from the published DDO
compute_service = ddo.get_service(ServiceTypes.CLOUD_COMPUTE)
print("Compute service definition: \n{}".format(json.dumps(compute_service.as_dictionary(), indent=2)))


# %% [markdown]
# Now let's run a python algorithm to do some analysis on this data
# Load the algorithm from file
algorithm_path = 'assets/sample_algorithm.json'
with open(algorithm_path) as f:
    algorithm_text = f.read()

# build the algorithm metadata object to use in the compute request
AlgorithmMetadata(
    {
        'language': 'python',
        'rawcode': algorithm_text,
        'container': {
            'tag': 'latest',
            'image': 'amancevice/pandas',
            'entrypoint': ''
        }
    }
)
# Create the service agreement for compute service
# Wait for the service approval
# Submit algorithm to start the compute job
# check the compute job status
# Wait for results


