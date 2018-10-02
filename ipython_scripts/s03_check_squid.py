#%% Imports

import pathlib
import squid_py.ocean as ocean
import sys
# %% Logging
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



#%% Instantiate the wrapper

# The contract addresses are loaded from file
PATH_CONFIG = pathlib.Path.cwd() / 'config_local.ini'
assert PATH_CONFIG.exists(), "{} does not exist".format(PATH_CONFIG)

ocn = ocean.Ocean(host='http://0.0.0.0', port=8545, config_path=PATH_CONFIG)

logging.info("Ocean smart contract node connected at {}".format(ocn.node_uri))
logging.info("{:>40} {}".format("Token contract address:", ocn.token.address))
logging.info("{:>40} {}".format("Authentication contract atddress:", ocn.auth.address))
logging.info("{:>40} {}".format("Market contract address:", ocn.market.address))

logging.info("Metadata store (provider) located at: {}".format(ocn.metadata.base_url))



#%%
