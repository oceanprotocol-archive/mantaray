# %% [markdown]
# With docker running, run this script to test the Ocean wrapper (squid-py).
# Instantiate the wrapper with the local config_local.ini.



# %% Imports

import pathlib
# import squid_py.ocean.ocean as ocean
from squid_py.ocean.ocean import Ocean
import sys
# from squid_py.utils.web3_helper import convert_to_bytes, convert_to_string, convert_to_text




# The contract addresses are loaded from file
PATH_CONFIG = pathlib.Path.cwd() / 'config_local.ini'
# PATH_CONFIG = pathlib.Path.cwd() / 'config_k8s_deployed.ini'

assert PATH_CONFIG.exists(), "{} does not exist".format(PATH_CONFIG)

#ocn = ocean.Ocean(host='http://0.0.0.0', port=8545, config_path=PATH_CONFIG)

ocn = Ocean(config_file=PATH_CONFIG)
#config = Config('config_local.ini')
#assert ocean.market.address == ocean.get_web3().toChecksumAddress(config.get(KEEPER_CONTRACTS, 'market.address'))

#%%
print("***OCEAN***")
print("{} accounts".format(len(ocn.accounts)))
print("\n***KEEPER NODE***")
print("Keeper node connected at {}".format(ocn.config.keeper_url))
print("Using ABI files from {}".format(ocn.config.keeper_path))
print("{:>40} {}".format("Token contract address:", ocn.keeper.token.address))
print("{:>40} {}".format("Authentication contract at address:", ocn.keeper.auth.address))
print("{:>40} {}".format("Market contract address:", ocn.keeper.market.address))
print("{:>40} {}".format("DID Registry contract address:", ocn.keeper.didregistry.address))

print("\n***METADATA STORE (aquarius)***")
print("Connect at: {}".format(ocn.metadata_store._base_url))

print("\n***SECRET STORE***")

print("\n***SERVICE HANDLER (brizo)***")

# %%

# %%