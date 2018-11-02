# %%
import requests
from squid_py import ocean
import sys
from pathlib import Path

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
formatter = logging.Formatter(FORMAT, DATE_FMT)

# Create handler and assign
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.handlers = [handler]
logger.debug("Logging started")

#%%

endpoints_dict = {
    'keeper-contracts': 'http://ac9959fcade8d11e89c320e965e714bc-777187363.us-east-1.elb.amazonaws.com:8545/',
    'pleuston': 'http://ac98d76bade8d11e89c320e965e714bc-981020006.us-east-1.elb.amazonaws.com:3000/',
    'aquarius': 'http://ac9905390de8d11e89c320e965e714bc-966378963.us-east-1.elb.amazonaws.com:5000',
    'aquarius_doc': 'http://ac9905390de8d11e89c320e965e714bc-966378963.us-east-1.elb.amazonaws.com:5000/api/v1/docs/',
}

def check_endpoint(endpoint, this_endpoints_dict, verb='GET', ):
    res = requests.request(verb, this_endpoints_dict[endpoint])
    logging.debug("{} : returns {}".format(endpoint, res.status_code))
    # res.content
    return res.status_code

check_endpoint('aquarius_doc', endpoints_dict)
check_endpoint('aquarius', endpoints_dict)
check_endpoint('keeper-contracts', endpoints_dict)
check_endpoint('pleuston', endpoints_dict)

#%%
config_path = Path.cwd() / '..' / '..' / 'config_k8s.ini'
config_path = Path.cwd() / 'config_k8s.ini'
assert config_path.exists()
ocn = ocean.Ocean(config_path)

