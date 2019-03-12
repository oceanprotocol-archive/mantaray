# Local development environment

The following guide will get you set up to run Mantaray locally in a development environment. 

## Section 1) Install dependencies 

First, decide which versions of the dependencies you wish to run. The table below summarizes the 

| component          | Type             | Date | PyPI     | Github     | Dockerhub | Kubernetes |
| ------------------ | ---------------- | ---- | -------- | ---------- | --------- | ---------- |
| squid-py           | Local -main API  |      | 0.2.22   | (develop)* | -         | -          |
| keeper-contracts   | ABI files        |      | 0.5.3    | (develop)* | -         | -          |
| mantaray_utilities | Library          |      | MISSING  | 0.1.0      | -         | -          |
| aquarius           | Service Endpoint |      | 0.1.5    |            |           |            |
| brizo              | Service Endpoint |      | 0.1.5    |            |           |            |
| Nile               | Ethereum network |      | (online) |            |           |            |

### Create a virtual environment

Create a new virtual environment using conda or pip. In this guide, conda is assumed. 

```
THISENVNAME=mantaray
conda create --name $THISENVNAME python
source activate $THISENVNAME
```

### Install dependencies 

#### Option 1: Install from PyPI

Activate the environment and install the ocean protocol API for python, called **squid-py**. This in turn installs the contract ABI files. 

```
pip install squid-py
pip install manta-utilities # TODO: NOT YET DEPLOYED TO PYPI!!
conda list | egrep 'keeper-contracts|squid-py|mantaray-utilities'
```

You should verify the versions of squid-py, and keeper-contracts. 

For developers wishing to convert IPython format into Jupyter format, the `jupytext` package can be used. The **mantaray** project has several other dependencies which are listed in the `setup.py` script.

#### Option 2: Install dependencies from github

Alternatively, you can install latest versions or branches from git. 

To install from a locally cloned git repository directory use;

```
pip install -e ~/ocn/squid-py
pip install -e ~/ocn/mantaray_utilities
```

Or install from a github branch;
```
pip install git+https://github.com/oceanprotocol/squid-py.git@develop
pip install git+https://github.com/oceanprotocol/mantaray_utilities.git@develop
```

More generally;
```
THIS_REPO=squid-py
THIS_BRANCH=develop
pip install --upgrade --force-reinstall git+https://github.com/oceanprotocol/$THIS_REPO.git@$THIS_BRANCH
```

Even more generally, see the /scripts/install_local.sh script which manages the installation process of multiple repositories and branches. 
```
source activate $THISENVNAME
source ./scripts/install_local.sh
```

Again, verify your versions: 

```
conda list | egrep 'keeper-contracts|squid-py|mantaray-utilities
```

## Section 2) Run the simulated Ocean stack

Ensure you have installed [docker](https://docs.docker.com/install/). 

`git clone` the [docker images](https://github.com/oceanprotocol/barge) repository and ensure you are in the master branch. 

Edit the `start_ocean.sh` script, and ensure that the `KEEPER_DEPLOY_CONTRACTS="true"`  variable is set. 

If you intend to publish Azure assets, edit the `brizo.env` file and enter your Azure credentials. 

Run the script with the following flags; `./start_ocean.sh --no-pleuston --local-spree-node`

This will run the following docker components:

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

You can view the running docker pods and versions of the components by executing `docker ps` at the terminal. 

## 3) Copy the ABI Artifact files

When running a local testnet (i.e. Spree network), you will **always** need to copy the deployed ABI files (contract artifacts). When running against a deployed blockchain (i.e. Nile, or ethereum testnet Kovan, etc.) you will need the exact ABI files which correspond to that blockchain. 

### 3.1 Local environment: 
The contract ABI `.json` files need to exist in the project root of the `mantaray` repo, in a folder called `\artifacts`. Copy all `.json`  files here from `~/.ocean/keeper-contracts/artifacts`. 

### 3.2 Deployed testnet

For Nile and Kovan networks, the contract ABI files have been packaged in [PyPI](https://pypi.org/project/keeper-contracts/), or go directly to the [github source](https://github.com/oceanprotocol/keeper-contracts) for the smart contracts . 

## 5) Setup publisher accounts 

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

## 6) Copy and review the configuration file

Copy the `config.ini` file to `config_local.ini`. This configuration file is passed into the main entrypoint of the library
the **Ocean** class. This configuration file should have the necessary configuration information to instantiate the class. 

Verify the following values refer to an unlocked account: 

```
PARITY_ADDRESS=
PARITY_ADDRESS=
PARITY_PASSWORD=
```

Verify that the URL's for Aquarius and Brizo match the exposed IP addresses in the docker network: 

```
aquarius.url = http://172.15.0.15:5000
brizo.url = http://172.15.0.17:8030
```

Similarly verify the URL's for keeper. 

This script will copy the ABI  files from the currently running 
docker container (keeper-contracts) into your *project directory*. 

## Section 7) Check your installation

The above steps should be sufficient to start testing the latest status of the Ocean Protocol stack in a local environment. 
The API can be explored in IPython, Jupyter Lab, or your preferred Python environment;

`from squid-py.ocean.ocean import Ocean`

`PATH_CONFIG = "/project/config_local.ini"` (Your path to a the configuration file)

`ocn = Ocean(config_file=PATH_CONFIG)`

Or review the script in `/mantaray/ipython_scripts/0_verify/check_squid.py`. 

