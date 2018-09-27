To install the latest environment for all local development;

```
THISENVNAME=mantaray4
conda create --name $THISENVNAME python
source activate $THISENVNAME
```

Install standard packages
```
conda install pandas
conda install boto3
```

Install ocean components from a local git repo
```
pip install ~/ocn/squid-py
pip install
```

Install Ocean components directly from a git branch
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

```