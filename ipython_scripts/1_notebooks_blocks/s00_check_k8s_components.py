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

import mantaray_utilities.config as manta_config
import mantaray_utilities.logging as manta_logging

#%%
# For this test, set the configuration environment variable for kubernetes.
# here it is hard-coded for IPython execution, but in general, it is set in your system environment.
# manta_config.name_deployment_type()
# os.environ['USE_K8S_CLUSTER'] = 'true'

manta_logging.logger.setLevel('INFO')

# Get the configuration file path for this environment
# CONFIG_INI_PATH = manta_config.get_config_file_path()
CONFIG_INI_PATH = os.environ['OCEAN_CONFIG_PATH']

logging.info("Configuration file selected: {}".format(CONFIG_INI_PATH))

import configparser
config = configparser.ConfigParser()
config.read(CONFIG_INI_PATH)


# %%
# The endpoints (microservices) are defined in the below dictionary

#%%
# For now, the endpoints are hard-coded by the dev-ops team.
endpoints_dict = {
    'aquarius': config['resources']['aquarius.url'],
    'brizo': config['resources']['brizo.url'],
    'Ethereum node': config['keeper-contracts']['keeper.url'],
    'secret_store' : config['keeper-contracts']['secret_store.url']
}
swagger_pages = dict()
swagger_pages['aquarius Swagger documentation'] = endpoints_dict['aquarius'] + '/api/v1/docs/'
swagger_pages['brizo Swagger documentation'] = endpoints_dict['brizo'] + '/api/v1/docs/'

def check_endpoint(endpoint_name, endpoint_url, verb='GET', ):
    """HTTP Request on the given URL"""
    res = requests.request(verb, endpoint_url)
    logging.debug("{} : returns {}".format(endpoint_name, res.status_code))
    return res
# %%
# The microscervices for MetaData storage (aquarius) and for service negotiation (brizo) have Swagger documentation :)
#%%
print("Aquarius MetaData storage API:", swagger_pages['aquarius Swagger documentation'])
print("Brizo Access API:", swagger_pages['brizo Swagger documentation'])

# %% [markdown]
# Finally, we will iterate over the endpoint and check for a response
#
#%%
flag_fail = False
for endpoint in endpoints_dict:
    with manta_logging.LoggerCritical():
        print("Checking {} at {}".format(endpoint, endpoints_dict[endpoint]))
        try:
            res = check_endpoint(endpoint, endpoints_dict[endpoint])
            if 'Content-Type' in res.headers:
                if res.headers['Content-Type'] == 'application/json':
                    if 'software' in res.json().keys() and 'version' in res.json().keys():
                        print("\t Success: {} v{}".format(res.json()['software'], res.json()['version']))
                else:
                    print("\t Success")
            else:
                print("\t Success")
        except:
            flag_fail = True
            print('\t Failed!')

if flag_fail:
    print("Failure in a component, please contact an administrator on our Gitter channel - https://gitter.im/oceanprotocol/Lobby")


