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


class LoggerCritical:
    def __enter__(self):
        my_logger = logging.getLogger()
        my_logger.setLevel("CRITICAL")
    def __exit__(self, type, value, traceback):
        my_logger = logging.getLogger()
        my_logger.setLevel("DEBUG")

#%%

endpoints_dict = {
    'keeper-contracts': 'http://ac9959fcade8d11e89c320e965e714bc-777187363.us-east-1.elb.amazonaws.com:8545/',
    'pleuston': 'http://ac98d76bade8d11e89c320e965e714bc-981020006.us-east-1.elb.amazonaws.com:3000/',
    'aquarius': 'http://ac3195287e10911e89c320e965e714bc-1875844701.us-east-1.elb.amazonaws.com:5000',
    'aquarius_doc': 'http://ac3195287e10911e89c320e965e714bc-1875844701.us-east-1.elb.amazonaws.com:5000/api/v1/docs/',
    'brizo': 'http://a3c6e8416e40b11e88a360a98afc4587-44361392.us-east-1.elb.amazonaws.com:8030/',
    'brizo_doc': 'http://a3c6e8416e40b11e88a360a98afc4587-44361392.us-east-1.elb.amazonaws.com:8030/api/v1/docs/',
    # 'secret_store_1' : "http://52.1.94.55",
    # 'secret_store_2': "http://54.156.6.164",
    # 'secret_store_3': "http://100.24.158.252",
    # 'empty' : "https://secret-store.dev-ocean-asdf.com",
    # 'secret_store_dns' : "https://secret-store.dev-ocean.com",
    'secret_store' : 'https://secret-store.dev-ocean.com/shadow/061299ac78ff49a19c1a284e7d3180c6131d88ce1fad45ca97e7f755acb694b1/7db43164e402dfddd1fb9bfc1f2ded608e2040962bb0f17af4728ba3c277772b1ba005f578293f9f3638e53bd6c365b34bc6e262f25686e7228a5becda4e197c01/2'

}

def check_endpoint(endpoint_name, endpoint_url, verb='GET', ):
    res = requests.request(verb, endpoint_url)
    logging.debug("{} : returns {}".format(endpoint_name, res.status_code))
    return res.status_code, res.content

for endpoint in endpoints_dict:
    with LoggerCritical():
        print("Checking {}".format(endpoint))
        try:
            code, status = check_endpoint(endpoint, endpoints_dict[endpoint])
            print('\t', endpoint, code, status)
        except:
            print('\t Failed!')

# check_endpoint('aquarius_doc', endpoints_dict)
# check_endpoint('aquarius', endpoints_dict)
# check_endpoint('keeper-contracts', endpoints_dict)
# check_endpoint('pleuston', endpoints_dict)
# check_endpoint('brizo', endpoints_dict)
# check_endpoint('brizo_doc', endpoints_dict)

#%%
config_path = Path.cwd() / '..' / '..' / 'config_k8s.ini'
config_path = Path.cwd() / 'config_k8s.ini'
assert config_path.exists()
ocn = ocean.Ocean(config_path)


