import pathlib
import sys
import logging
import time

from squid_py.ocean.ocean import Ocean

loggers_dict = logging.Logger.manager.loggerDict

logger = logging.getLogger()
logger.handlers = []

# Set level
logger.setLevel(logging.INFO)

FORMAT = "%(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(FORMAT, DATE_FMT)
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.handlers = [handler]
logger.debug("Logging started")

# The contract addresses are loaded from file
PATH_CONFIG = pathlib.Path.cwd() / 'config_local.ini'
assert PATH_CONFIG.exists(), "{} does not exist".format(PATH_CONFIG)

ocn = Ocean(config_file=PATH_CONFIG)

# %% Test the accounts
assert len(ocn.accounts) > 0
print (ocn.accounts)
unlocked_account_name = '0x00Bd138aBD70e2F00903268F3Db08f2D25677C9e'
if unlocked_account_name in ocn.accounts:
    unlocked_account = ocn.accounts.get(unlocked_account_name)
else:
    unlocked_account = next(iter(ocn.accounts.values()))

assert unlocked_account.ether_balance > 0

ocn_balance = unlocked_account.ocean_balance
ocn_rain = 10
print(ocn_balance)
unlocked_account.request_tokens(ocn_rain)
time.sleep(8)
print(unlocked_account.ocean_balance)
assert unlocked_account.ocean_balance - ocn_rain == ocn_balance

