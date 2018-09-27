install_branch() {
	THIS_ORG=$1
	THIS_REPO=$2
	THIS_BRANCH=$3
	echo "Installing package from $THIS_BRANCH of $THIS_ORG/$THIS_REPO"
	pip install --upgrade --force-reinstall git+https://github.com/$THIS_ORG/$THIS_REPO.git@$THIS_BRANCH
}

install_branch oceanprotocol squid-py develop

install_branch oceanprotocol osmosis-aws-driver develop

install_branch MarcusJones py2nb master
