[![banner](https://raw.githubusercontent.com/oceanprotocol/art/master/github/repo-banner%402x.png)](https://oceanprotocol.com)

# mantaray

>    🐙 [Data Science level 2 ](https://placeholder.com) high level implementation management for (Python).
>    [oceanprotocol.com](https://oceanprotocol.com)

[![Travis (.com)](https://img.shields.io/travis/com/oceanprotocol/mantaray.svg)](https://travis-ci.com/oceanprotocol/mantaray)
[![Codacy coverage](https://img.shields.io/codacy/coverage/de067a9402c64b989c76b27cfc74fefe.svg)](https://app.codacy.com/project/ocean-protocol/mantaray/dashboard)
[![PyPI](https://img.shields.io/pypi/v/mantaray.svg)](https://pypi.org/project/mantaray/)
[![GitHub contributors](https://img.shields.io/github/contributors/oceanprotocol/mantaray.svg)](https://github.com/oceanprotocol/mantaray/graphs/contributors)

---

## Table of Contents

  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Quickstart](#quickstart)
  - [Environment variables](#environment-variables)
  - [Code style](#code-style)
  - [Testing](#testing)
  - [New Version](#new-version)
  - [License](#license)

---

## Features
![manta](doc/img/manta_small.jpg)

Manage assets for data science in an interactive shell, as part of the
typical data science workflow.
 - Register and upload datasets and their descriptive metadata to;
    - [ ] Local components and local ethereum blockchain (Ganache)
    - [ ] Cloud-hosted components and cloud ethereum blockchain (Ganache)
    - [ ] Cloud-hosted components and test-network ethereum blockchain (Kovan test network)
 - Discover and download datasets from;
    - [ ] Local components and local ethereum blockchain (Ganache)
    - [ ] Cloud-hosted components and cloud ethereum blockchain (Ganache)
    - [ ] Cloud-hosted components and test-network ethereum blockchain (Kovan test network)

Designed to be used with an interactive Python shell, for example the IPython
Read–Eval–Print Loop (REPL) found in [Jupyter Notebooks](http://jupyter.org/)
and other editors.

## Deployment


| **component**          	| **Date**   	| **Github** 	| **PyPI** 	| **Dockerhub** 	| **Kubernetes**    	| *Trilobite notes*                                    	|
|------------------------	|------------	|------------	|----------	|---------------	|-------------------	|------------------------------------------------------	|
| squid-py               	| Nov. 09    	| v0.2.4     	| 0.2.4    	| N/A           	| N/A               	| PR - Event subscription/callbacks - Wed              	|
|                        	|            	|            	|          	|               	|                   	| PR - Secret store - Wed                              	|
|                        	|            	|            	|          	|               	|                   	| PR - Functions for end2end - Friday                  	|
|                        	|            	|            	|          	|               	|                   	| PR - other?                                          	|
| keeper-contracts       	| Nov. 8     	| 0.3.19     	| 0.3.19   	| v0.3.19       	| v0.3.19           	| OK                                                   	|
| aquarius               	| Nov. 5     	| v0.1.12    	| N/A      	| v0.1.12       	| v0.1.12           	| OK                                                   	|
| brizo                  	| latest     	| latest     	| missing! 	| latest        	| latest            	| Update soon, depends on squid-py / execute agreement 	|
| secret-store-client-py 	| latest     	| ??         	| ??       	| ??            	| (Running on EC2!) 	| ??                                                   	|
| pleuston               	| October... 	| latest     	| N/A      	| latest        	| latest            	| Need tag? Update?                                    	|


## Local usage

###  Setup local environment and packages
Create a new virtual environment. 

A conda environment can also be used, it may cause a conflict in certain conda env packages (certifi, etc.?). 

Activate the environment and install the ocean stack API for python, called **squid-py**. 
The latest version is installed with `pip install squid-py 0.2.14`. 

TODO: UPDATE -> The **mantaray** project has several other dependencies which are *currently* listed in the `setup.py` script. 

For end users, no other packages are required. 

For developers, the `jupytext` package can be used to export an IPython script the Jupyter Lab format.

### Get the simulated Ocean Protocol local components

git clone the [docker images](https://github.com/oceanprotocol/docker-images) github repository and switch to the `feature/refactor` branch. 

### Setup publisher accounts 

#### Brizo, the publisher service
As a Publisher, the service endpoint called 'brizo' will need to be correctly configured. 

This configuration is found in the docker-images repo which you have just cloned. 

Edit this file: `brizo.env`

The account information must match your publisher account.

Update the following values to an unlocked account:
 - PARITY_ADDRESS=
 - PARITY_PASSWORD=
 
#### MS Azure account, for hosting files
Currently, only Microsoft Azure is supported for hosting files. 

Complete the following account details to ensure the asset is published and served: 
 - AZURE_ACCOUNT_NAME=
 - AZURE_ACCOUNT_KEY=
 - AZURE_RESOURCE_GROUP=
 - AZURE_LOCATION=
 - AZURE_CLIENT_ID=
 - AZURE_CLIENT_SECRET=
 - AZURE_TENANT_ID=
 - AZURE_SUBSCRIPTION_ID=


### Start the simulated Ocean Protocol local components

With the above configuration complete, you are ready to start the local components in docker. 

A shell script is provided in the docker-images repo; `start-ocean.sh`.

The recommended configuration is `./start_ocean.sh --latest --local-parity-node`

This will run the following components:
 - Backend database: `mongo`
 - The parity-node: `oceanprotocol/parity-ethereum:beta`
 - The secret-store:`oceanprotocol/parity-ethereum:master`
 - A secret store proxy for CORS: `nginx:alpine` 
 - The smart contracts deployed into Ganache: `oceanprotocol/keeper-contracts:latest`
 - The Metadata Store: `oceanprotocol/aquarius:latest`
 - The services provider: `oceanprotocol/brizo:latest`

The parity node is deployed with accounts which are LOCKED. These must be UNLOCKED in the script to use. 

### Copy the config.ini file
Copy the `config.ini` file to `config_local.ini`. This configuration file is passed into the main entrypoint of the library
the **Ocean** class. This configuration file should have the necessary configuration information to instantiate the class. 

### Extract the smart contract ABI's
Execute the script in your *project directory* i.e. `~/git/mantaray`.

`. ./scripts/wait_for_migration_and_extract_keeper_artifacts.sh`

This script will copy the ABI (Application Binary Interface) files from the currently running 
docker container (keeper-contracts) into your *project directory*. 

### Check your installation

The above steps should be sufficient to start testing the latest status of the Ocean Protocol stack in a local environment. 
The API can be explored in IPython, Jupyter Lab, or your preferred Python environment;

`from squid-py.ocean.ocean import Ocean`

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
1. Metadata is prepared in a .json format according to [link](link)
1. The dataset is uploaded to S3 using [osmosis_aws_driver.S3_Plugin](https://github.com/oceanprotocol/osmosis-aws-driver)
	1. Credentials are managed by AWS/boto3
	1. Call the S3_Plugin.upload() method
	1. Record the URL
	1. Check policy and permissions
1. 

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

## Code style

The information about code style in python is documented in this two links [python-developer-guide](https://github.com/oceanprotocol/dev-ocean/blob/master/doc/development/python-developer-guide.md)
and [python-style-guide](https://github.com/oceanprotocol/dev-ocean/blob/master/doc/development/python-style-guide.md).
​    
## Testing

Automatic tests are setup via Travis, executing `tox`.
Our test use pytest framework.

## New Version

The `bumpversion.sh` script helps to bump the project version. You can execute the script using as first argument {major|minor|patch} to bump accordingly the version.

## License

```
Copyright 2018 Ocean Protocol Foundation Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

```
