#!/usr/bin/env bash
#
# This script is used to pip install requirements directly from GitHub
# Specify the branch to stay up to date on latest changes on a new branch

install_branch() {
    # Given a github path (organization, repo, branch)
    # pip install the repo
	THIS_ORG=$1
	THIS_REPO=$2
	THIS_BRANCH=$3
	echo 
	echo "Force-installing package from $THIS_BRANCH branch of $THIS_ORG/$THIS_REPO"
	echo
	pip install --upgrade --force-reinstall --ignore-installed git+https://github.com/$THIS_ORG/$THIS_REPO.git@$THIS_BRANCH
}


#install_branch oceanprotocol squid-py develop
install_branch oceanprotocol squid-py v0.2.5

install_branch oceanprotocol aquarius v0.1.2

install_branch oceanprotocol osmosis-driver-interface develop

install_branch oceanprotocol osmosis-aws-driver develop

install_branch oceanprotocol keeper-contracts develop
