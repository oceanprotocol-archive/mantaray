

## Local development environment

Create a virtual environment

```
THISENVNAME=mantaray
conda create --name $THISENVNAME python
source activate $THISENVNAME
```

### Install dependencies from PyPI

Install the main API, which in turn installs the contract ABI files

```
pip install squid-py
pip install manta-utilities # TODO: NOT YET DEPLOYED!
conda list | egrep 'keeper-contracts|squid-py|mantaray-utilities'
```

You should verify the versions of squid-py, and keeper-contracts. 

### Install dependencies from github

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