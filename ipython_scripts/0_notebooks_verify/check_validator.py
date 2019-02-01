# %% [markdown]
#

# %%
## Imports
import logging
from pathlib import Path
logging.basicConfig(level=logging.DEBUG)

import plecos.plecos as plecos
# from plecos import validate
# import plecos.plecos
# plecos.validate('asdf')
# print(plecos)
# print(plecos.__file__)
PATH_DATA_ROOT = Path("~/DATA").expanduser()
path_data_dir = PATH_DATA_ROOT / 'British_birdsong'
path_metadata = path_data_dir / 'metadata.json'
plecos.validate(path_metadata)
# plecos.validate_cli

