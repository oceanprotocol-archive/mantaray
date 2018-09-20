#%%

import osmosis_aws_driver.data_S3_plugin as ocean_s3
dir(ocean_s3)
config = dict()
config['region'] = 'eu-central-1'
ocn_s3 = ocean_s3.S3_Plugin(config)

ocn_s3.list_buckets()

#%%