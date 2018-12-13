# %% [markdown]
# # Welcome to Manta Ray
# ## Data Science powered by Ocean Protocol
#
# The **Manta Ray** scripts provide a guided tour of Ocean Protocol in an interactive Jupyter Notebook environment.
#
# Scripts are first written in regular Python (with the `#%%` cell demarcation formatting) in the
# [mantaray](https://github.com/oceanprotocol/mantaray) repo, and then converted into Jupyter Notebooks, `.ipynb`.
# A seperate GitHub repository holds these converted notebooks, to provide an uncluttered directory for JupyterHub. This repo,
# [mantaray_jupyter](https://github.com/oceanprotocol/mantaray_utilities), is then cloned into the environment you are using.
#
# As a Data Scientist, you may feel free to copy these notebooks or parts thereof to build a new Notebook. Or if you
# prefer to work in pure python, please go to the mantaray source repo and review the python scripts in the `/ipython` directory.
#
#%% [markdown]
# ### For developers:
# Cloud components are used to simulate Ocean Protocol. Local docker components are [also available](https://github.com/oceanprotocol/docker-images).
#
# The main import is the [squid-py](https://github.com/oceanprotocol/squid-py) ([PyPI link](https://pypi.org/project/squid-py/))
# Ocean Python API. This in-turn depends on downloading the Application Binary Interface files for the deployed Ethereum smart contracts. These ABI files are
# deployed to PyPI as the [keeper-contracts](https://pypi.org/project/keeper-contracts/) package.
#
# Instructions for setting a developer environment are available at our documentation website TODO: (releasing soon!)

# %% [markdown]
# ## Meanwhile, on the dry dock...
# Let's get ship-shape! First, check your dependencies using the cell below. Install any missing components into your environment as necessary.

#%% [markdown]
# **squid-py** is your friendly interface to **Ocean Protocol**
#%%
import squid_py
print("squid_py", squid_py.__version__)

#%% [markdown]
# An set of [utility methods](https://github.com/oceanprotocol/mantaray_utilities) is installed, for extra functionality for the Data Science community
#%%
import mantaray_utilities
print("mantaray_utilities", mantaray_utilities.__version__)
# %% [markdown]
## Ship's manifest
# In the left pane, several scripts are loaded, designed to walk you through the Ocean Protocol stack.
#
# First, check the functionality of the cloud components with `check_k8s_components`.
#
# Then, you can instantiate the main class for interacting with Ocean, the aptly named **Ocean** class in `squid-py`, in the `check_squid` notebook.
#
# The next set of notebooks each focus on a main aspect of Ocean Protocol. These can be composed into a complete data science pipeline.
#
# Weigh anchor, and good luck sailing into Ocean Protocol!
