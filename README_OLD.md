# TODO: Update below information

## Examples

[Test the components](/mantaray/ipython_scripts/m00_test_connections.py)

## Prerequisites

During development, install directly from the locally downloaded repo and
selected branch as follows;

```
source activate env_name
cd ~/folder_to_repo/
pip install -e .
```

For deployed components, use your favourite python package and environment
management and PyPi directly (via requirements.txt).

- S3 command line tool, for uploading data - [osmosis_aws_driver](https://github.com/oceanprotocol/osmosis-aws-driver)
- The Ocean Protocol interface, [squid-py](https://github.com/oceanprotocol/squid-py), 
- Which in turn interfaces with the following docker images, running locally (using docker-compose);
  - Offline blockchain smart-contracts [oceanprotocol/keeper-contracts](https://hub.docker.com/r/oceanprotocol/keeper-contracts/)
  - Metadata Store interface [oceanprotocol/aquarius](https://hub.docker.com/r/oceanprotocol/aquarius/), which depends on (by default) : 
    - [mongodb](https://github.com/mongodb/)
    - [bigchaindb](https://github.com/bigchaindb/bigchaindb)
    - [tendermint](https://github.com/tendermint/tendermint)

## Quickstart: Publishing data on local components

To publish data, the following steps are performed;

1. The dataset is formatted and prepared locally
2. Metadata is prepared in a .json format according to [link](link)
3. The dataset is uploaded to S3 using [osmosis_aws_driver.S3_Plugin](https://github.com/oceanprotocol/osmosis-aws-driver)
   1. Credentials are managed by AWS/boto3
   2. Call the S3_Plugin.upload() method
   3. Record the URL
   4. Check policy and permissions
4. 

## Quickstart: Discovering and downloading data on local components



## Developers notes

### Create a new virtual environment

Using pip, conda, etc.

Activate the environment.

### Install the [osmosis-aws-driver](https://github.com/oceanprotocol/osmosis-aws-driver) S3 plugin to manage datasets on S3

Install the package itself, from local git repo, or online from Github;
`~/ocn/osmosis-aws-driver/pip install -e .`

`pip install git+https://github.com/tangentlabs/django-oscar-paypal.git@issue/34/oscar-0.6`

`conda env update --name mantaray1`

`keeper-contracts` running



## Environment variables

TODO
When you want to instantiate an Oceandb plugin you can provide the next environment variables:

- **$CONFIG_PATH** 
- **$MODULE** 
- **$DB_HOSTNAME** 
- **$DB_PORT**

...