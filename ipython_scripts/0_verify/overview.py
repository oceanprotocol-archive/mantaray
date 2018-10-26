# %% [markdown]
# # MANTARAY
# ## Data Science powered by **Ocean Protocol**

# %% [markdown]
# The **Mantaray** scripts provide a guided tour of Ocean Protocol in an interactive environment.
#
# The scripts are designed to be executed in an 'IPython' interactive console.
#
# The popular Jupyter Notebook format is supported.
#
# Alternatively, you can run the scripts in other IPython environments.
#
# The scripts are generated in two formats: .py scripts with the # %% cell demarcation convention, or the auto-converted .ipynb format for i.e. Jupyter Notebook.
#
# These scripts also serve as a catalog of building blocks for building more complex user stories and applications.

# %% [markdown]
# Jupyter Lab can use different python environments (kernels)
# For easiest use, install the `ipykernel` package into your environment:
#
# `pip install ipykernel` or `conda install ipykernel`
#
# Then, install the kernel using the IPython command; `ipython kernel install --user --name=projectname`
#
# TODO: Check this error in ipykernel deps
#
#  If error on above command, try `pip install 'prompt-toolkit==1.0.15'`
# Then, `python -m ipykernel install --user --name mantaray3 --display-name "Python (mantaray3)" `

# %% [markdown]
# ## Meanwhile, on the dry dock...
# Let's get ship-shape! First, check your dependencies using the cell below. Install any missing components into your environment as necessary.

# %%
# The AWS SDK
import boto3
print( "boto3", boto3.__version__ )

# The docker python utility can be used to manage your local docker configuration
import docker
print("docker", docker.__version__)

# Alternatively, you may connect to the Kubernetes cluster for testing
# TODO: k8s util check

# Or, you can connect to the Ethereum test net
# TODO: test net util check

# Metamask is used to access the Ethereum network
# TODO: metamask util

# squid-py is your friendly interface to **Ocean Protocol**
import squid_py
print("squid_py", squid_py.__version__)

# %% [markdown]
## Ship's manifest

# %% [markdown]
# ### <span style="color:Aqua">AWS S3 management</span>
# #### check_aws_s3
# Test your connection to S3
# #### process_catalogue
# Using your AWS account, manage your data assets

# %% [markdown]
# ### <span style="color:Aqua">Local docker verification</span>
# #### check_docker
# If using a local simulation of the blockchain and ocean protocol infrastructure, this script can help you verify your containers

# %% [markdown]
# ### <span style="color:Aqua">Local docker verification</span>
# #### check_squid
# Got squid?
# #### play_with_your_squid
# Start verifying fundamental interaction with Ocean Protocol.


#%% [markdown]
# OLD ...
# %%
# Rank:
# Ensign -
# Able seaman
# Before embarking across Ocean Protocol, let's get ship-shape with the following pre-requisites;
# Pre

# %% [markdown]
#
# Ready the sails!


# %% [markdown]
#
# Inspection
