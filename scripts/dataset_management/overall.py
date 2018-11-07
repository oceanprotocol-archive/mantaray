import shutil
from pathlib import Path
import zipfile
import logging
import random
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
# %% Iterate over
dict_ds = dict()
for dir_ds in datasets:
    path_ds = path_data_root / dir_ds
    assert path_ds.exists(), path_ds
    dict_ds[dir_ds] = dict()
    dict_ds[dir_ds]['full'] = path_ds / 'full'
    dict_ds[dir_ds]['sample'] = path_ds / 'sample'

# %%
dict_ds["Humpback_identification"]["full"]
train_zip = dict_ds["Humpback_identification"]["full"] / 'train.zip'
assert train_zip.exists()
NUM_SAMPLES = 10
SAMPLE_DIR = dict_ds["Humpback_identification"]["sample"]
assert SAMPLE_DIR.exists()

files = list()
with zipfile.ZipFile(train_zip, "r") as zf:
    files = zf.namelist()
    sample_files = [random.choice(files) for i in range(NUM_SAMPLES)]
    for sample_f in sample_files:
        with zf.open(sample_f) as this_file:
            print(this_file)
            res = Path(this_file.name)
            path_out = SAMPLE_DIR / (str(res.stem) + str(res.suffix))
            with open(path_out, 'wb') as out_file:
                print(out_file)
                # out_file.write(zf.read(this_file))
                # out_file.write(zf.read(this_file))
                shutil.copy(this_file,path_out)

            # k, open():j

logging.debug(f"Found {len(files)} files in {train_zip}")
logging.debug(f"Extracted {len(sample_files)} images for sample".format())


# %%
with zipfile.ZipFile(train_zip) as z:
    with z.open('train/f185b7aa.jpg') as zf, open('train/f185b7aa.jpg', 'wb') as f:
        shutil.copyfileobj(zf, f)


    # for name in f.namelist():
    #     data = f.read(name)
    #     print(name, len(data), repr(data[:10]))


