"""
Ensure we can instantiate the Ocean object
"""

def test_ocean_instance(ocean_instance):
    ocean_instance.print_config()
    assert ocean_instance.keeper.token is not None

    # There is ONE Web3 instance
    assert ocean_instance.keeper.market.web3 is ocean_instance.keeper.auth.web3 is ocean_instance.keeper.token.web3
    assert ocean_instance._web3 is ocean_instance.keeper.web3

    ocean_instance.print_config()

