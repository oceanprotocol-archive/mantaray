# %%
import requests
import sys
import os
import logging

# Import mantaray and the Ocean API (squid)
from squid_py.ocean import ocean
import mantaray_utilities.config as manta_config
import mantaray_utilities.logging as manta_logging

#%%
# For this test, set the configuration environment variable
os.environ['USE_K8S_CLUSTER'] = 'true'
manta_config.name_deployment_type()

# When running in IPython, ensure the project path is correct
# This may vary according to your environment
manta_logging.logger.setLevel('INFO')

# Get the configuration file path
CONFIG_INI_PATH = manta_config.get_config_file_path()
# manta_config.get_project_path() /
# Add the local utilities package
# utilities_path = PATH_PROJECT / 'script_fixtures'
# assert utilities_path.exists()
# utilities_path = str(utilities_path.absolute())
# if utilities_path not in sys.path:
#     sys.path.append(utilities_path)



#%%

endpoints_dict = {
    'keeper-contracts': 'http://52.1.94.55:8545',
    'pleuston': 'http://ac98d76bade8d11e89c320e965e714bc-981020006.us-east-1.elb.amazonaws.com:3000/',
    'aquarius': 'http://ac8b5e618ef0511e88a360a98afc4587-575519081.us-east-1.elb.amazonaws.com:5000',
    'brizo': 'http://ac8b8cc42ef0511e88a360a98afc4587-974193642.us-east-1.elb.amazonaws.com:8030',
    'secret_store' : 'https://secret-store.dev-ocean.com'

}
endpoints_dict['aquarius Swagger documentation'] = endpoints_dict['aquarius'] + '/api/v1/docs/'
endpoints_dict['brizo Swagger documentation'] = endpoints_dict['brizo'] + '/api/v1/docs/'
def check_endpoint(endpoint_name, endpoint_url, verb='GET', ):
    res = requests.request(verb, endpoint_url)
    logging.debug("{} : returns {}".format(endpoint_name, res.status_code))
    return res.status_code, res.content

for endpoint in endpoints_dict:
    with manta_logging.LoggerCritical():
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

with manta_logging.LoggerCritical():
    ocn = ocean.Ocean(CONFIG_INI_PATH)
print("*******************")
print("Ocean successfully instantiated with kubernetes!")


