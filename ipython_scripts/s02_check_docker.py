#%% Imports
import docker
client = docker.from_env()
import subprocess
# import subprocess
# import pathlib
# import squid_py.ocean as ocean
import sys
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

#%% Check running docker images using SDK
client = docker.from_env()
client.containers.list()
for container in client.containers.list():
   print(container.name, container.status)
   print(container.image.tags)
   print(container.labels)
# container.logs()

#%% Low level client
# Get the APIClient for running commands
api_client = docker.APIClient(base_url='unix://var/run/docker.sock')
# Get the docker image running the smart contracts
container_keeper_contracts = client.containers.get('docker_keeper-contracts_1')

# This is the python script to be executed in the running image
python_script = r"import sys, json; print(json.load(open('/keeper-contracts/artifacts/OceanMarket.development.json', 'r'))['address'])"

# Wrap the script in quotes (string) and add the python shell command
command = r"python -c " + '"' + python_script + '"'

# Create and run the command
ex = api_client.exec_create(container=container_keeper_contracts.id , cmd=command)
api_client.exec_start(ex)
#%%

container_keeper_contracts = client.containers.get('docker_keeper-contracts_1')

exe = client.exec_create(container=container_keeper_contracts.id, cmd=cmds)
exe_start= cli.exec_start(exec_id=exe, stream=True)

for val in exe_start:
    print (val)


#%%

container_keeper_contracts = client.containers.get('docker_keeper-contracts_1')
# container_keeper_contracts.exe
client.exec_

market=$(docker exec -it docker_keeper-contracts_1 python -c "import sys, json; print(json.load(open('/keeper-contracts/artifacts/OceanMarket.development.json', 'r'))['address'])")
