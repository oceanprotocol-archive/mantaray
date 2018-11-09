# %%
import requests
from squid_py import ocean
import sys
from pathlib import Path

# %% Logging
""" 
"""
import logging
logger = logging.getLogger()

# Set level
logger.setLevel(logging.DEBUG)
FORMAT = "%(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(FORMAT, DATE_FMT)

# Create handler and assign
logger.handlers = []
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.handlers = [handler]
logger.debug("Logging started")

#%%

endpoints_dict = {
    'keeper-contracts': 'http://ac9959fcade8d11e89c320e965e714bc-777187363.us-east-1.elb.amazonaws.com:8545/',
    'pleuston': 'http://ac98d76bade8d11e89c320e965e714bc-981020006.us-east-1.elb.amazonaws.com:3000/',
    'aquarius': "http://ac3195287e10911e89c320e965e714bc-1875844701.us-east-1.elb.amazonaws.com:5000",
    'aquarius_doc': 'http://ac3195287e10911e89c320e965e714bc-1875844701.us-east-1.elb.amazonaws.com:5000/api/v1/docs/',
    'brizo': 'http://a3c6e8416e40b11e88a360a98afc4587-44361392.us-east-1.elb.amazonaws.com:8030',
    'brizo_doc': 'http://a3c6e8416e40b11e88a360a98afc4587-44361392.us-east-1.elb.amazonaws.com:8030/api/v1/docs/',
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
check_endpoint('brizo', endpoints_dict)
check_endpoint('brizo_doc', endpoints_dict)
#%%
config_path = Path.cwd() / '..' / '..' / 'config_k8s.ini'
config_path = Path.cwd() / 'config_k8s.ini'
assert config_path.exists()
ocn = ocean.Ocean(config_path)


