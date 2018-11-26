"""
Ensure we can instantiate the Ocean object
"""
from squid_py.ocean import ocean
import os

def test_ocean_instance():
    path_config = 'config_local.ini'
    os.environ['CONFIG_FILE'] = path_config
    ocn = ocean.Ocean(os.environ['CONFIG_FILE'])

    assert ocn.keeper.token is not None

    # There is ONE Web3 instance
    assert ocn.keeper.market.web3 is ocn.keeper.auth.web3 is ocn.keeper.token.web3
    assert ocn._web3 is ocn.keeper.web3

    ocn.print_config()

