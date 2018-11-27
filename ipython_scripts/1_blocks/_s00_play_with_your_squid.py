# %% [markdown]

# <p><center>Ocean Protocol</p>
# <p><center>Trilobite pre-release 0.1</center></p>
# <img src="https://oceanprotocol.com/static/media/logo-white.7b65db16.png" alt="drawing" width="200" align="center"/>
# </center>

# %%
# Ocean Protocol
#
# Trilobite release
#
# <img src="https://oceanprotocol.com/static/media/logo-white.7b65db16.png" alt="drawing" width="200"/>
# <img src="https://oceanprotocol.com/static/media/logo.75e257aa.png" alt="drawing" width="200"/>
#
# %% [markdown]
# # Test functionality of squid-py wrapper.

# %% [markdown]
# <img src="https://3c1703fe8d.site.internapcdn.net/newman/gfx/news/hires/2017/mismatchedey.jpg" alt="drawing" width="200" align="center"/>

# %% [markdown]
# ## Section 1: Import modules, and setup logging

# %% [markdown]
# Imports
#%%
from pathlib import Path
import squid_py.ocean as ocean_wrapper
# from squid_py.utils.web3_helper import convert_to_bytes, convert_to_string, convert_to_text, Web3Helper
import sys
import random
import json
import os
from pprint import pprint
import configparser
# import squid_py.ocean as ocean
from squid_py.ocean.ocean import Ocean
from squid_py.ocean.asset import Asset
import names
import secrets
from squid_py.ddo import DDO
from unittest.mock import Mock
import squid_py
print("Squid API version:", squid_py.__version__)
import unittest

# %% [markdown]
# Logging
# %%
import logging
loggers_dict = logging.Logger.manager.loggerDict
logger = logging.getLogger()
logger.handlers = []
# Set level
logger.setLevel(logging.INFO)
FORMAT = "%(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(FORMAT, DATE_FMT)
# Create handler and assign
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.handlers = [handler]
logger.info("Logging started")
# %% [markdown]
# ## Section 2: Instantiate the Ocean Protocol interface

#%%
# The contract addresses are loaded from file
# CHOOSE YOUR CONFIGURATION HERE
PATH_CONFIG = Path.cwd() / 'config_local.ini'
# PATH_CONFIG = Path.cwd() / 'config_k8s_deployed.ini'
assert PATH_CONFIG.exists(), "{} does not exist".format(PATH_CONFIG)

ocn = Ocean(PATH_CONFIG)
logging.info("Ocean smart contract node connected ".format())
