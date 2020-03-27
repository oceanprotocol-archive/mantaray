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
# %%
# Standard imports
import json
import logging
import os
import time
from pathlib import Path

# Import mantaray and the Ocean API (squid)
import squid_py
from ocean_keeper.web3_provider import Web3Provider
from mantaray_utilities.misc import get_algorithm_example
from mantaray_utilities.user import create_account
from ocean_utils.agreements.service_factory import ServiceDescriptor
from ocean_utils.agreements.service_types import ServiceTypes
from ocean_utils.utils.utilities import get_timestamp
from squid_py.models.algorithm_metadata import AlgorithmMetadata
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
from mantaray_utilities import logging as manta_logging, config
from mantaray_utilities.misc import get_metadata_example

from pprint import pprint

# Setup logging
manta_logging.logger.setLevel('INFO')
print("squid-py Ocean API version:", squid_py.__version__)

# %%
# Get the configuration file path for this environment
OCEAN_CONFIG_PATH = Path(os.path.expanduser(os.environ['OCEAN_CONFIG_PATH']))
assert OCEAN_CONFIG_PATH.exists(), "{} - path does not exist".format(OCEAN_CONFIG_PATH)
logging.critical("Configuration file selected: {}".format(OCEAN_CONFIG_PATH))
logging.critical("Deployment type: {}".format(config.get_deployment_type()))
logging.critical("Squid API version: {}".format(squid_py.__version__))
# %%
# Prepare the provider address to use when creating the asset and service agreement
web3 = Web3Provider.get_web3()
provider_address = web3.toChecksumAddress(os.environ.get('MARKET_PLACE_PROVIDER_ADDRESS', ''))
print(f'Will be using provider (Brizo) address: {provider_address}')
# %%
# Instantiate Ocean with the default configuration file.
configuration = Config(OCEAN_CONFIG_PATH)
ocn = Ocean(configuration)
# faucet is used to request ether from the TESTNET (e.g. the Nile testnet)
faucet_url = ocn.config.get('keeper-contracts', 'faucet.url')
scale = 10**18
# %% [markdown]
# We need accounts for the publisher and consumer, let's make new ones
# %%
# Publisher account (will be filled with some TESTNET ether automatically)
publisher_acct = create_account(faucet_url, wait=True)
print("Publisher account address: {}".format(publisher_acct.address))
# ensure Ocean token balance
if ocn.accounts.balance(publisher_acct).ocn == 0:
    ocn.accounts.request_tokens(publisher_acct, 100)
print("Publisher account Testnet 'ETH' balance: {:>6.1f}".format(ocn.accounts.balance(publisher_acct).eth/scale))
print("Publisher account Testnet Ocean balance: {:>6.1f}".format(ocn.accounts.balance(publisher_acct).ocn/scale))
# %%
# Consumer account (same as above, will have some TESTNET ether added)
consumer_account = create_account(faucet_url, wait=True)
print("Consumer account address: {}".format(consumer_account.address))
if ocn.accounts.balance(consumer_account).ocn/scale < 100:
    ocn.accounts.request_tokens(consumer_account, 100)
# Verify both ocean and ether balance
print("Consumer account Testnet 'ETH' balance: {:>6.1f}".format(ocn.accounts.balance(consumer_account).eth/scale))
print("Consumer account Testnet Ocean balance: {:>6.1f}".format(ocn.accounts.balance(consumer_account).ocn/scale))

# %% [markdown]
# ### Section 1: Publish the asset with compute service
# %%
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
    13, 3600, publisher_acct.address, get_timestamp(), provider_attributes
)
service_endpoint = 'http://localhost:8030/api/v1/brizo/services/compute'
template_id = ocn.keeper.template_manager.create_template_id(
    ocn.keeper.template_manager.SERVICE_TO_TEMPLATE_NAME['compute']
)
service_descriptor = ServiceDescriptor.compute_service_descriptor(attributes, service_endpoint, template_id)
# %%
# Get example of Meta Data from file
metadata = get_metadata_example()
# Print the entire (JSON) dictionary
# pprint(metadata)

# With this metadata object prepared, we are ready to publish the asset into Ocean Protocol.
ddo = ocn.assets.create(
    metadata,
    publisher_acct,
    [service_descriptor],
    providers=[publisher_acct.address],
    use_secret_store=False
)
registered_did = ddo.did
print("New asset registered at", registered_did)
# %% [markdown]
# Let's take a look at the compute service from the published DDO
# %%
compute_service = ddo.get_service(ServiceTypes.CLOUD_COMPUTE)
pprint("Compute service definition: \n{}".format(json.dumps(compute_service.as_dictionary(), indent=2)))

# %% [markdown]
# ### Section 2: Preparing the algorithm that will be run
# Grab the algorithm example from mantaray_utilities
# %%
algorithm_text = get_algorithm_example()
print(f'algorithm: \n{algorithm_text}')
# build the algorithm metadata object to use in the compute request
algorithm_meta = AlgorithmMetadata(
    {
        'language': 'python',
        'rawcode': algorithm_text,
        'container': {
            'tag': 'latest',
            'image': 'amancevice/pandas',
            'entrypoint': 'python $ALGO'
        }
    }
)
# print(f'algorith meta: {algorithm_meta.as_dictionary()}')

# %% [markdown]
# ### Section 3: Subscribe to the compute service
# Now we can prepare for running the remote compute, first we need to start an agreement to buy the service
# %%
# First step in buying a service is placing the order which creates
# and starts the service agreement process, consumer payment is
# processed automatically once the agreement is created successfully.
agreement_id = ocn.compute.order(
    ddo.did,
    consumer_account,
    provider_address=publisher_acct.address
)
print(f'Got agreementId: {agreement_id}')
# %%
# We should verify that the agreement is created successfully
event = ocn.keeper.agreement_manager.subscribe_agreement_created(agreement_id, 20, None, (), wait=True)
if event:
    print(f'Got agreement event {agreement_id}: {event}')
else:
    print(f'Cannot find agreement event, could be a VM transaction error.')
# %%
# Wait for payment transaction
payment_locked_event = ocn.keeper.lock_reward_condition.subscribe_condition_fulfilled(agreement_id, 30, None, [], wait=True)
assert payment_locked_event, 'payment event was not found'
# %%
# and wait for service agreement approval from the provider end
compute_approval_event = ocn.keeper.compute_execution_condition.subscribe_condition_fulfilled(agreement_id, 30, None, [], wait=True)
assert compute_approval_event, 'compute agreement is not approved yet.'

# %% [markdown]
# ### Section 4: Run the algorithm remotely on the dataset
# Now that the agreement is approved by the provider, we can start the compute job
# %%
# Submit algorithm to start the compute job
try:
    job_id = ocn.compute.start(agreement_id, ddo.did, consumer_account, algorithm_meta=algorithm_meta)
    print(f'compute job started: jobId={job_id}')
except Exception as err:
    print(f'error: {err}')
    job_id = ''
# %%
# check the compute job status
status = ocn.compute.status(agreement_id, job_id, consumer_account)
print(f'compute job status: {status}')
# %% [markdown]
# Wait for results
#
# %%
trials = 0
result = ocn.compute.result(agreement_id, job_id, consumer_account)
while not result.get('urls'):
    print(f'result not available yet, trial {trials}/30, '
          f'status is: {ocn.compute.status(agreement_id, job_id, consumer_account)}')
    time.sleep(10)
    result = ocn.compute.result(agreement_id, job_id, consumer_account)
    trials = trials + 1
    if trials > 20:
        print(f'the run is taking too long, I give up.')
        break
print(f'got result from compute job: {result}')
