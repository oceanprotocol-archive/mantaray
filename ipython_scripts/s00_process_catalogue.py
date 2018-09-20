# General imports
import sys
import os
#import glob
import pandas as pd
import hashlib

#%% Logging
import logging
loggers_dict = logging.Logger.manager.loggerDict
 
logger = logging.getLogger()
logger.handlers = []

# Set level
logger.setLevel(logging.DEBUG)

# Create formatter

#FORMAT = "%(asctime)s - %(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"
FORMAT = "%(asctime)s L%(levelno)s: %(message)s"

DATE_FMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(FORMAT, DATE_FMT)

# Create handler and assign
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.handlers = [handler]
logger.critical("Logging started")

#%% IO
PATH_PROJECT_BASE = r"/home/batman/ocn/plankton-datascience"
assert os.path.exists(PATH_PROJECT_BASE)
PATH_DATA_CATALOGUE = os.path.join(PATH_PROJECT_BASE,'planktonDS_data_seeding/OceanDataSets_master catalog r00.csv')
assert os.path.exists(PATH_DATA_CATALOGUE)

PATH_DATA_CATALOGUE_CLEAN = os.path.join(PATH_PROJECT_BASE,'planktonDS_data_seeding/OceanDataSets_master catalog clean.csv')

#%% Load the data catalogue
df = pd.read_csv(PATH_DATA_CATALOGUE)
df.columns

#%%############################################################################
# Column: SizeGB
###############################################################################

# Cleanup function
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
# Drop non-numeric size
mask_numeric = df.loc[:,'SizeGB'].apply(is_number)
df = df.drop(df[mask_numeric==False].index)
logging.debug("SizeGB Col: Dropped {} non-numeric sizes".format(sum(mask_numeric==False)))

# Convert size to numeric
df.loc[:,'SizeGB'] = pd.to_numeric(df.loc[:,'SizeGB'])
logging.debug("SizeGB Col: Converted size to {}".format(df.loc[:,'SizeGB'].dtype))

# Drop NaN sizes
mask_size_not_na = df.loc[:,'SizeGB'].isna() == False
num_dropped = sum(mask_size_not_na == False)
df = df[mask_size_not_na]
logging.debug("SizeGB Col: Dropped {} size=NaN records".format(num_dropped))

#%% 
#df_describe = df.describe(include='all')
#df_info = df.info()

#%%############################################################################
# Column: Download Link
###############################################################################

# Drop non-unique links
num_records = len(df)
#df = df.loc[:,'Download Link'].drop_duplicates(subset='Download Link',keep='first')
df = df.drop_duplicates(subset='Download Link',keep='first')
logging.debug("Download Link Col: {} records with duplicate links dropped".format(num_records-len(df)))


# Drop NAN
num_records = len(df)
df = df.dropna(axis=0, subset = ['Download Link'])
logging.debug("Download Link Col: {} records with duplicate links dropped".format(num_records-len(df)))

#%%
df_describe = df.describe(include='all')

#%%############################################################################
# Column: Formats
###############################################################################

# Cleaning function
def rename_value(df,colname,original_str, new_str):
    mask= df.loc[:,colname] == original_str
    df.loc[mask,colname]  = new_str
    logging.debug("Formats Col: Renamed {} {} records from {} to {}".format(sum(mask),colname,original_str, new_str))
    return df

df = rename_value(df,'Format','.tar', 'tar')
df = rename_value(df,'Format','.tgz', 'tgz')

# Subset on formats
select_formats=['zip','csv','gzip','tar','tgz']
df_sub = df[df.loc[:,'Format'].isin(select_formats)]
len(df_sub)
logging.debug("Formats Col: Selected {} of {} records, formats: {}".format(len(df_sub), len(df), select_formats))


#%%############################################################################
# Summarize and save
###############################################################################

df_sub_describe = df_sub.describe(include='all')

#%% Add a hash
df_sub['hash'] = df_sub.apply(lambda x: hashlib.sha256(repr(tuple(x)).encode('utf-8')).hexdigest(), axis = 1)
assert(sum(df_sub['hash'].duplicated())==0)
logging.debug("Added a HASH ID column".format())

#%% Save the file
df_sub.to_csv(PATH_DATA_CATALOGUE_CLEAN)
