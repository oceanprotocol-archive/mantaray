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

###  1) Setup local environment and install packages

Create a new virtual environment using i.e. conda or pip. 

Activate the environment and install the ocean protocol API for python, called **squid-py**. 

The latest version is installed with `pip install squid-py 0.2.14`. 

Install the utilities library for mantaray `pip install git+https://github.com/oceanprotocol/mantaray_utilities.git`

For developers, the `jupytext` package can be used to export an IPython script the Jupyter Lab format. The **mantaray** project has several other dependencies which are *currently* listed in the `setup.py` script.

### 2) Run the simulated Ocean Protocol local components in Docker

git clone the [docker images](https://github.com/oceanprotocol/docker-images) repository and ensure you are in the master branch. 

Edit the `start_ocean.sh` script, and ensure that the `KEEPER_DEPLOY_CONTRACTS="true"`  variable is set. 

If you intend to publish Azure assets, edit the `brizo.env` file and enter your Azure credentials. 

Run the script with the following flags; `./start_ocean.sh --no-pleuston --local-spree-node`

This will run the following components:

- Backend database: `mongo`
- The parity-node: `oceanprotocol/parity-ethereum:beta`
- The secret-store:`oceanprotocol/parity-ethereum:master`
- A secret store proxy for CORS: `nginx:alpine` 
- The smart contracts deployed into Ganache: `oceanprotocol/keeper-contracts:latest`
- The Metadata Store: `oceanprotocol/aquarius:latest`
- The services provider: `oceanprotocol/brizo:latest`

The parity node is deployed with accounts which are LOCKED. These must be UNLOCKED with a password to use. 

The relevant docker-compose files will begin downloading the images, and starting the containers. The ethereum smart contracts will be *compiled* and *migrated* in the `keeper-contracts` container. These contracts will also be copied to your home directory in a `~/.ocean/keeper-contracts/artifacts` folder. 

In this folder ensure that there exists several `.json` files with the word `spree` (referring to the local docker simulated testnet). These are the contract *artifacts* or ABI's (Application Binary Interface) which are the signatures of the deployed smart contracts. 

### 3) Copy the smart contract ABI's to the project folder

The contract ABI `.json` files need to exist in the project root of the `mantaray` repo, in a folder called `\artifacts`. Copy all `.json`  files here from `~/.ocean/keeper-contracts/artifacts`. 

### 4) Setup publisher accounts 

As a Publisher, the service endpoint called 'brizo' will need to be correctly configured. 

This configuration is found in the docker-images repo which you have just cloned. 

Edit this file: `brizo.env`

The account information must match your publisher account. 

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

### 5) Copy and review the configuration file

Copy the `config.ini` file to `config_local.ini`. This configuration file is passed into the main entrypoint of the library
the **Ocean** class. This configuration file should have the necessary configuration information to instantiate the class. 

Verify the following values refer to an unlocked account: 
```PARITY_ADDRESS=
PARITY_ADDRESS=
PARITY_PASSWORD=
```

Verify that the URL's for Aquarius and Brizo match the exposed IP addresses in the docker network: 

```
aquarius.url = http://172.15.0.15:5000
brizo.url = http://172.15.0.17:8030
```

This script will copy the ABI  files from the currently running 
docker container (keeper-contracts) into your *project directory*. 

### 6) Check your installation

The above steps should be sufficient to start testing the latest status of the Ocean Protocol stack in a local environment. 
The API can be explored in IPython, Jupyter Lab, or your preferred Python environment;

`from squid-py.ocean.ocean import Ocean`

`PATH_CONFIG = "/project/config_local.ini"` (Your path to a the configuration file)

`ocn = Ocean(config_file=PATH_CONFIG)`

Or review the script in `/mantaray/ipython_scripts/0_verify/check_squid.py`. 



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
