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
    'keeper-contracts': 'http://52.1.94.55:8545',
    'pleuston': 'http://ac98d76bade8d11e89c320e965e714bc-981020006.us-east-1.elb.amazonaws.com:3000/',
    'aquarius': 'http://ac8b5e618ef0511e88a360a98afc4587-575519081.us-east-1.elb.amazonaws.com:5000',
    'brizo': 'http://ac8b8cc42ef0511e88a360a98afc4587-974193642.us-east-1.elb.amazonaws.com:8030',
    'secret_store' : 'https://secret-store.dev-ocean.com'

}
endpoints_dict['aquarius_doc'] = endpoints_dict['aquarius'] + '/api/v1/docs/'
endpoints_dict['brizo_doc'] = endpoints_dict['brizo'] + '/api/v1/docs/'
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


