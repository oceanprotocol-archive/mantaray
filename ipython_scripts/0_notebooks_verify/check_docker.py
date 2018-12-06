# %% [markdown]

# This script is used to check your local docker images.

# Two methods can be used - shell commands with subprocess. Popen, or
# use the docker SDK (docker-py) to manage and inspect local configuration and running images.

# A function is declared to wrap executing a command insider an image which retrieves the contract addresses
# from the contract artifact JSON files (ABIs). Use this to confirm that your local configuration (as
# specified in config_local.ini) matches the deployed images.

# %% Imports
import docker
import subprocess
import sys
from pprint import pprint

# %% Logging
import logging
import mantaray_utilities.logging as manta_logging

# %% Check running docker images from command line
# s = subprocess.check_output('docker ps', shell=True).wait()
s = subprocess.Popen("docker ps" + "", shell=True).wait()
print(s)

# %% Client, and low level API client
# High level client
client = docker.from_env()
# Get the APIClient for running commands
low_level_api_client = docker.APIClient(base_url='unix://var/run/docker.sock')

# %% Check running docker images using SDK
with manta_logging.LoggerCritical():
    for container in client.containers.list():
        print(f"Docker container {container.name} is {container.status}")
        print('\tTags:', container.image.tags)
        # print(container.labels)
        # print("\n")
    # container.logs()

# %% Get addresses from images
def get_address(api_client, container_id,contract_name):
    network_name = 'ocean_poa_net_local'
    # This is the python script to be executed in the running image
    python_script = r"import sys, json; print(json.load(open('/keeper-contracts/artifacts/{}.{}.json', 'r'))['address'])".format(contract_name,network_name)

    # Wrap the script in quotes (string) and add the python shell command
    command = r"python -c " + '"' + python_script + '"'

    # Create and run the command
    ex = api_client.exec_create(container=container_id, cmd=command)

    return api_client.exec_start(ex)

# Get the docker image running the smart contracts, by searching on the name
container_keeper_contracts = [c for c in client.containers.list() if 'keeper-contracts' in c.name][0]

addresses=dict()
addresses['market.address'] = get_address(low_level_api_client, container_keeper_contracts.id,'OceanMarket').decode("utf-8").rstrip()
addresses['auth.address'] = get_address(low_level_api_client, container_keeper_contracts.id,'OceanAuth').decode("utf-8").rstrip()
addresses['token.address'] = get_address(low_level_api_client, container_keeper_contracts.id,'OceanToken').decode("utf-8").rstrip()
addresses['didregistry.address'] = get_address(low_level_api_client, container_keeper_contracts.id,'DIDRegistry').decode("utf-8").rstrip()

print("Artifact addresses retrieved:")
pprint(addresses)


