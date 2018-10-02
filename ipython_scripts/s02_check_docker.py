#%% Imports
import docker
client = docker.from_env()
import subprocess
# import subprocess
# import pathlib
# import squid_py.ocean as ocean
import sys
from pprint import pprint
#%% Logging
import logging

loggers_dict = logging.Logger.manager.loggerDict

logger = logging.getLogger()
logger.handlers = []

# Set level
logger.setLevel(logging.DEBUG)

# FORMAT = "%(asctime)s - %(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"
# FORMAT = "%(asctime)s %(levelno)s: %(module)30s %(message)s"
FORMAT = "%(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"

DATE_FMT = "%Y-%m-%d %H:%M:%S"
DATE_FMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(FORMAT, DATE_FMT)

# Create handler and assign
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.handlers = [handler]
logger.debug("Logging started")
#%% Check running docker images from command line
# s = subprocess.check_output('docker ps', shell=True).wait()
s = subprocess.Popen("docker ps" + "", shell=True).wait()
print(s)

#%% Client, and low level API client
# High level client
client = docker.from_env()
# Get the APIClient for running commands
low_level_api_client = docker.APIClient(base_url='unix://var/run/docker.sock')

#%% Check running docker images using SDK
for container in client.containers.list():
    print(container.name, container.status)
    print(container.image.tags)
    print(container.labels)
# container.logs()
#%% Get addresses from images
def get_address(api_client, container_id,contract_name):

    # This is the python script to be executed in the running image
    python_script = r"import sys, json; print(json.load(open('/keeper-contracts/artifacts/{}.development.json', 'r'))['address'])".format(contract_name)

    # Wrap the script in quotes (string) and add the python shell command
    command = r"python -c " + '"' + python_script + '"'

    # Create and run the command
    ex = api_client.exec_create(container=container_id, cmd=command)

    return api_client.exec_start(ex)

# Get the docker image running the smart contracts
container_keeper_contracts = client.containers.get('docker_keeper-contracts_1')
addresses=dict()
addresses['market.address'] = get_address(low_level_api_client,container_keeper_contracts.id,'OceanMarket').decode("utf-8").rstrip()
addresses['auth.address'] = get_address(low_level_api_client,container_keeper_contracts.id,'OceanToken').decode("utf-8").rstrip()
addresses['token.address'] = get_address(low_level_api_client,container_keeper_contracts.id,'OceanAuth').decode("utf-8").rstrip()

pprint(addresses)


