from pathlib import Path
import os
import logging
import pandas as pd

# %% Paths
path_input = Path(os.environ.get("INPUTS", "/data/inputs"))
path_output = Path(os.environ("OUTPUTS", "/data/outputs"))
path_logs = Path(os.environ.get("LOGS", "/data/logs"))

input_files = list(path_input.iterdir())
assert len(input_files) == 1, "Currently, only 1 input file is supported."
path_input_file = input_files.pop()

path_output_file = path_output / 'summary.csv'

# %% Check all paths
assert path_input_file.exists(), "Can't find required mounted path: {}".format(path_input_file)
assert path_input_file.is_file() | path_input_file.is_symlink(), "/volumes/input/dataset must be a file"
assert path_output.exists(), "Can't find required mounted path: {}".format(path_output)
# assert path_logs.exists(), "Can't find required mounted path: {}".format(path_output)
print(f"Selected input file: {path_input_file} {os.path.getsize(path_input_file)/1000/1000} MB")
print(f"Target output folder: {path_output}")

# %% Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', handlers=[logging.StreamHandler()])

logging.info("Starting logging")

# %% Load data
logging.debug("Loading {}".format(path_input_file))
with open(path_input_file, 'rb') as fh:
    df = pd.read_csv(fh)

logging.debug("Loaded {} records into DataFrame".format(len(df)))

summary = df.describe()
logging.debug("Built summary of records.")
summary.to_csv(path_output_file)
logging.debug("Wrote results to {}".format(path_output_file))

logging.debug("FINISHED ALGORITHM EXECUTION")
