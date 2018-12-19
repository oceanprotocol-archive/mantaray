# %% [markdown]
# # Welcome to Manta Ray
# ## Data Science powered by Ocean Protocol
#
# The **Manta Ray** notebooks provide a guided tour of Ocean Protocol in an interactive JupyterLab environment.
#
# Scripts are first written in regular Python (with the `#%%` cell demarcation format). You see the source
# [mantaray](https://github.com/oceanprotocol/mantaray) Github repository. These scripts are then converted into Jupyter Notebooks, `.ipynb`.
# A seperate GitHub repository holds these converted notebooks, to provide an uncluttered directory for the JupyterHub server. This repo,
# [mantaray_jupyter](https://github.com/oceanprotocol/mantaray_utilities), is then cloned into the environment you are currently using.
#
# As a Data Scientist or Data Engineer, you may wish to copy these notebooks or parts thereof to build a new notebook for your pipeline. Or if you
# prefer to work in pure Python, please go to the mantaray source repo and review the `.py` scripts in the `/ipython` directory.
#
# As a Developer, you can use the notebooks as a tutorial and demonstration in working with Ocean Protocol.
#
# %% [markdown]
# Notes on architecture:
#
# The present JupyterLab instance is running on your own virtual machine,
#
# The Ocean Protocol stack is deployed to the cloud to simulate the blockchain and middle-ware.
# These endpoints are configured in the `config_jupyter.ini` file.
#
# Local docker components are [also available](https://github.com/oceanprotocol/docker-images) for developers.
#
# The primary imported library is called [squid-py](https://github.com/oceanprotocol/squid-py)
# ([PyPI link](https://pypi.org/project/squid-py/)), the
# Ocean Protocol Python API. Squid is your interface to the deployed smart contracts.
#
# This in-turn depends on downloading the Application Binary Interface files for the deployed Ethereum smart contracts.
# These ABI files are
# deployed to PyPI as the [keeper-contracts](https://pypi.org/project/keeper-contracts/) package.
#
# Instructions for setting a developer environment are available at our documentation website TODO: (releasing soon!)
#
# For questions, help, bug reports, etc., please contact us in our [Gitter Channel](https://gitter.im/oceanprotocol/Lobby)
# %% [markdown]
# ## Meanwhile, on the dry dock...
# Let's get ship-shape! First, check your dependencies using the cell below. Install any missing components into your
# environment as necessary.

#%% [markdown]
# **squid-py** is your friendly interface to **Ocean Protocol**

#%%
import squid_py
print("squid_py", squid_py.__version__)

#%% [markdown]
# The main class of

#%% [markdown]
# An set of [utility methods](https://github.com/oceanprotocol/mantaray_utilities) is installed, for extra functionality
# for the Data Science community.

#%%
import mantaray_utilities
print("mantaray_utilities", mantaray_utilities.__version__)

# %% [markdown]
# Some of the main utilities are the `config` module, and the `user` module, for simulating a User.

#%%
# The config module makes it easier to manage local and deployed notebooks and components.
import mantaray_utilities.config
# The deployment type is discovered using environment variables
# JUPYTER_DEPLOYMENT    - For JupyterHub/Lab, and deployed cloud components
# USE_K8S_CLUSTER       - For running scripts locally, but still connecting to the deployed cloud components
# DEFAULT               - Running scripts locally, and running the components locally in Docker

print("***Deployment Settings***")

# The deployment is retrieved using;
print("Deployment environment:", mantaray_utilities.config.get_deployment_type())

# Each deployment type has a 'project' root path;
print("Project path:", mantaray_utilities.config.get_project_path())

# And each deployment type has a default configuration script;
print("Configuration file:", mantaray_utilities.config.get_config_file_path())

# %% [markdown]
## Ship's manifest
# In the left pane, several scripts are loaded, designed to walk you through the Ocean Protocol stack.
#
# First, check the functionality of the cloud components with `check_k8s_components`. This script will iterate and
# check the status over each of each deployed URL.
#
# Then, you can instantiate the main class for interacting with Ocean, the aptly named **Ocean** class in `squid-py`,
# in the `check_squid` notebook.
#
# The next set of notebooks each focus on a main aspect of Ocean Protocol. These can be composed into a complete data
# science pipeline.
#
# Weigh anchor, and smooth sailing into Ocean Protocol!
#
# For questions, help, bug reports, etc., please contact us in our [Gitter Channel](https://gitter.im/oceanprotocol/Lobby)