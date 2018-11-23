import shutil
from pathlib import Path
import zipfile
import logging
import random
import pandas as pd
# %%
import logging
loggers_dict = logging.Logger.manager.loggerDict
logger = logging.getLogger()
logger.handlers = []
# Set level
logger.setLevel(logging.DEBUG)
FORMAT = "%(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(FORMAT, DATE_FMT)
# Create handler and assign
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.handlers = [handler]
logger.info("Logging started")


# %%
# The datasets are first saved locally, for convenience
# Each dataset is stored in a directory as follows;
datasets =[
    "Humpback_identification",
    "Humpback_fluke_location",
    "Monkey_Species",
    ]

path_data_root = Path.home() / "DATA"
# %% Iterate over each DS
dict_ds = dict()
for dir_ds in datasets:
    path_ds = path_data_root / dir_ds
    assert path_ds.exists(), path_ds
    dict_ds[dir_ds] = dict()
    dict_ds[dir_ds]['full'] = path_ds / 'full'
    dict_ds[dir_ds]['sample'] = path_ds / 'sample'

# %% Extract single images into /sample

# The full dataset zip file
train_zip = dict_ds["Humpback_identification"]["full"] / 'train.zip'
assert train_zip.exists()

# The sample subset
NUM_SAMPLES = 10
SAMPLE_DIR = dict_ds["Humpback_identification"]["sample"]
assert SAMPLE_DIR.exists()

# Open the zip file
with zipfile.ZipFile(train_zip) as z:
    # Get all file names, select a subset
    files = z.namelist()
    sample_files = [random.choice(files) for i in range(NUM_SAMPLES)]
    for sample_f in sample_files:
        # Create the target path
        # print(sample_f)
        res = Path(sample_f).name
        print(res)
        # path_out = SAMPLE_DIR / (str(res.stem) + str(res.suffix))
        path_out = SAMPLE_DIR / res
        # Open the specific sample file, and the target path
        with z.open(sample_f) as zf, open(path_out, 'wb') as f:
            print(zf, f)
            shutil.copyfileobj(zf, f)
logging.debug(f"Found {len(files)} files in {train_zip}")
logging.debug(f"Extracted {len(sample_files)} images for sample".format())


# %% Apply the labels

train_csv = dict_ds["Humpback_identification"]["full"] / 'train.csv'
assert train_csv.exists()


