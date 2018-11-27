"""Test fixtures for PyTest"""
import os
import pytest
from squid_py.ocean import ocean

def make_ocean_instance():
    path_config = 'config_local.ini'
    os.environ['CONFIG_FILE'] = path_config
    return ocean.Ocean(os.environ['CONFIG_FILE'])

@pytest.fixture
def ocean_instance():
    ocean.Client = SecretStoreClientMock
    ocn = make_ocean_instance()
    ocean.requests = BrizoMock(ocn, list(ocn.accounts)[0])

    return ocn

