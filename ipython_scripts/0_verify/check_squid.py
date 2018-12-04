# %% [markdown]
# With docker running, run this script to test the Ocean wrapper (squid-py).
# Instantiate the wrapper with the local config_local.ini.

# %% Imports
import pathlib
PATH_PROJECT = pathlib.Path.cwd()
from squid_py.ocean.ocean import Ocean

# The contract addresses are loaded from file
PATH_CONFIG = PATH_PROJECT / 'config_local.ini'
# PATH_CONFIG = PATH_PROJECT / 'config_k8s_deployed.ini'

assert PATH_CONFIG.exists(), "{} does not exist".format(PATH_CONFIG)

ocn = Ocean(config_file=PATH_CONFIG)

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