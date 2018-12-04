# %% [markdown]

# <p><img src="https://oceanprotocol.com/static/media/banner-ocean-03@2x.b7272597.png" alt="drawing" width="800" align="center"/>

# %% [markdown]

# <h1><center>Ocean Protocol - Manta Ray project</center></h1>
# <h3><center>Decentralized Data Science and Engineering, powered by Ocean Protocol</center></h3>
# <p>Version 0.2 - Trilobite preview</p>
# <p><a href="https://github.com/oceanprotocol/mantaray">mantaray on Github</a></p>
# <p>

#%% [markdown]
# <p>

#%%
PATH_PROJECT
# %%
import pathlib
# Ensure paths are correct in Jupyter Hub
# The PATH_PROJECT path variable must be the root of the project folder
PATH_PROJECT = pathlib.Path.cwd() # By default the root is the current working directory
# But if run as a Jupyter Notebook, the cwd will be one of:
script_folders = ['0_verify', '1_blocks', '2_use_cases', '3_demos']

if any(folder == pathlib.Path.cwd().parts[-1] for folder in script_folders):
    # Go up to the parent
    PATH_PROJECT = pathlib.Path.cwd().parents[0]

#%% [markdown]
# <p>