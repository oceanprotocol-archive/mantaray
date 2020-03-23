#%%
# Standard imports
import logging

# Import mantaray and the Ocean API (squid)
import random
import squid_py
from squid_py.ocean.ocean import Ocean
from squid_py.config import Config
from util.user import password_map
from pprint import pprint
import requests

# Setup logging
from util import config, user, logging as manta_logging

manta_logging.logger.setLevel('INFO')

#%%
# Get the configuration file path for this environment
CONFIG_INI_PATH = config.get_config_file_path()
logging.critical("Deployment type: {}".format(config.get_deployment_type()))
logging.critical("Configuration file selected: {}".format(CONFIG_INI_PATH))
logging.critical("Squid API version: {}".format(squid_py.__version__))

#%%
# Instantiate Ocean with the default configuration file.
configuration = Config(CONFIG_INI_PATH)
ocn = Ocean(configuration)

# %% [markdown]
# ### Section 1: A publisher account in Ocean

#%%
# Get a publisher account
path_passwords = config.get_project_path() / 'passwords.csv'
passwords = user.load_passwords(path_passwords)

publisher_acct = random.choice([acct for acct in ocn.accounts.list() if password_map(acct.address, passwords)])
publisher_acct.password = password_map(publisher_acct.address, passwords)
assert publisher_acct.password

#%%
print("Publisher account address: {}".format(publisher_acct.address))
print("Publisher account balance:", ocn.accounts.balance(publisher_acct).ocn)

# %% [markdown]
# Your account will need some Ocean Token to make real transactions, let's ensure that you are funded!

# %%
# ensure Ocean token balance
if ocn.accounts.balance(publisher_acct).ocn == 0:
    ocn.accounts.request_tokens(publisher_acct, 100)

# %% [markdown] ########################################################################################################
# GET METADATA
# ######################################################################################################################
# %%
this_url = "https://s3.amazonaws.com/datacommons-seeding-us-east/10_Monkey_Species_Small/metadata_OEP8.json"
response = requests.get(this_url)
if response.status_code == 200:
    metadata = response.json()
else:
    raise AssertionError("Failed to get metadata.")

pprint(metadata)
print("Name of Asset:", metadata['main']['name'])
print("Price of Asset:", metadata['main']['price'])

for i, file in enumerate(metadata['main']['files']):
    print("Asset link {}: {}".format(i, file['url']))

# %% [markdown] ########################################################################################################
# REGISTER
# ######################################################################################################################
# %%
ddo = ocn.assets.create(metadata, publisher_acct)
registered_did = ddo.did
print("New asset registered at", registered_did)

# %% [markdown] ########################################################################################################
# CONSUME
# ######################################################################################################################
# %%
# Use the Query function to get all existing assets
basic_query = {"service": {"$elemMatch": {"metadata": {"$exists": True}}}}
all_ddos = ocn.assets.query(basic_query)
assert len(all_ddos), "There are no assets registered, go to s03_publish_and_register!"
print("There are {} assets registered in the metadata store.".format(len(all_ddos)))
assert len(all_ddos), "There are no assets registered, go to s03_publish_and_register!"

# Get a DID for testing
selected_ddo = all_ddos[-1]
selected_did = all_ddos[-1].did
print("Selected asset name:", all_ddos[-1].metadata['main']['name'])
print("Selected DID:", selected_did)

# %% [markdown]
#
#%%
service_agreement_id = ocn.assets.order(selected_ddo.did, '0', publisher_acct)
print('New service agreement id:', service_agreement_id)
#%%
