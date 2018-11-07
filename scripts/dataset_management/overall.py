from pathlib import Path

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


