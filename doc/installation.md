

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
conda list | egrep 'keeper-contracts|squid-py'
```

You should verify the versions of squid-py, and keeper-contracts. 

### Install dependencies from github

Alternatively, you can install latest versions or branches from git. 

Install ocean components from a local git repository directory 

```
pip install ~/ocn/squid-py
```

Or install from a github branch
```
pip install git+https://github.com/oceanprotocol/squid-py.git@develop
```

More generally,
```
THIS_REPO=squid-py
THIS_BRANCH=develop
pip install --upgrade --force-reinstall git+https://github.com/oceanprotocol/$THIS_REPO.git@$THIS_BRANCH
```

Even more generally, see the /scripts/install_local.sh script to manage the installation process.
```
source activate $THISENVNAME
source ./scripts/install_local.sh
```