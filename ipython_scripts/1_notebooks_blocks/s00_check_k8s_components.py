# %% [markdown]
# # Pre-sail checklist - Ocean protocol component status
# With simulated Kubernetes endpoints deployed, this script will make a simple
# HTTP request to each, and report the status returned.
#
# %%
# Standard imports
import requests
import os
import logging

# Import mantaray and the Ocean API (squid)
from squid_py.ocean import ocean
import mantaray_utilities.config as manta_config
import mantaray_utilities.logging as manta_logging

#%%
# For this test, set the configuration environment variable for kubernetes.
# here it is hard-coded for IPython execution, but in general, it is set in your system environment.
manta_config.name_deployment_type()
os.environ['USE_K8S_CLUSTER'] = 'true'
manta_logging.logger.setLevel('INFO')

# Get the configuration file path for this environment
CONFIG_INI_PATH = manta_config.get_config_file_path()
logging.info("Configuration file selected: {}".format(CONFIG_INI_PATH))

#%%

# For now, the endpoints are hard-coded by the dev-ops team.
endpoints_dict = {
    'keeper-contracts': 'http://52.1.94.55:8545',
    'aquarius': 'http://ac8b5e618ef0511e88a360a98afc4587-575519081.us-east-1.elb.amazonaws.com:5000',
    'brizo': 'http://ac8b8cc42ef0511e88a360a98afc4587-974193642.us-east-1.elb.amazonaws.com:8030',
    'secret_store' : 'https://secret-store.dev-ocean.com'
}
# endpoints_dict['aquarius Swagger documentation'] = endpoints_dict['aquarius'] + '/api/v1/docs/'
# endpoints_dict['brizo Swagger documentation'] = endpoints_dict['brizo'] + '/api/v1/docs/'

def check_endpoint(endpoint_name, endpoint_url, verb='GET', ):
    """HTTP Request on the given URL"""
    res = requests.request(verb, endpoint_url)
    logging.debug("{} : returns {}".format(endpoint_name, res.status_code))
    return res


# %% [markdown]
# Iterate over the defined endpoints.
#
# TODO: secret_store fails, but scripts still run
#%%
for endpoint in endpoints_dict:
    with manta_logging.LoggerCritical():
        print("Checking {}".format(endpoint))
        try:
            res = check_endpoint(endpoint, endpoints_dict[endpoint])
            if res.headers['Content-Type'] == 'application/json':
                if 'software' in res.json().keys() and 'version' in res.json().keys():
                    print("\t Success: {} v{}".format(res.json()['software'], res.json()['version']))
            else:
                print("\t Success: <no status endpoint>")
        except:
            print('\t Failed!')

