"""
With docker running, run this script to test the Ocean wrapper (squid-py).

Instantiate the wrapper with the local config_local.ini.
"""

# %% Imports

import pathlib
# import squid_py.ocean.ocean as ocean
from squid_py.ocean.ocean import Ocean
import sys
# from squid_py.utils.web3_helper import convert_to_bytes, convert_to_string, convert_to_text

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

# %% Instantiate the wrapper

# The contract addresses are loaded from file
PATH_CONFIG = pathlib.Path.cwd() / 'config_local.ini'
PATH_CONFIG = pathlib.Path.cwd() / 'config_k8s_deployed.ini'

assert PATH_CONFIG.exists(), "{} does not exist".format(PATH_CONFIG)

#ocn = ocean.Ocean(host='http://0.0.0.0', port=8545, config_path=PATH_CONFIG)

ocn = Ocean(config_file=PATH_CONFIG)
#config = Config('config_local.ini')
#assert ocean.market.address == ocean.get_web3().toChecksumAddress(config.get(KEEPER_CONTRACTS, 'market.address'))

# logging.info("Ocean smart contract node connected at {}".format(ocn.node_uri))
# logging.info("_keeper_url {}".format(ocn.))
# logging.info("_keeper_path {}".format(ocn.))
# logging.info("_gas_limit {}".format(ocn.))
# logging.info("_provider_url {}".format(ocn.))


logging.info("{:>40} {}".format("Token contract address:", ocn.keeper.token.address))
logging.info("{:>40} {}".format("Authentication contract at address:", ocn.keeper.auth.address))
logging.info("{:>40} {}".format("Market contract address:", ocn.keeper.market.address))
logging.info("{:>40} {}".format("DID Registry contract address:", ocn.keeper.didregistry.address))

logging.info("Metadata store (provider) located at: {}".format(ocn.metadata._base_url))

# %%

# %%