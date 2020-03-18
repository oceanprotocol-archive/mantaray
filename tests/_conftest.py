"""Test fixtures for PyTest"""
import os
import pytest
from squid_py import Config
from squid_py.ocean import ocean


def make_ocean_instance():
    path_config = 'config_local.ini'
    os.environ['CONFIG_FILE'] = path_config
    configuration = Config(path_config)
    return ocean.Ocean(configuration)


@pytest.fixture
def ocean_instance():
    return make_ocean_instance()

