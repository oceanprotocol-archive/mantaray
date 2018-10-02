#%% Imports
import docker
client = docker.from_env()

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

# container.logs()
