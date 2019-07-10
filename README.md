[![banner](https://raw.githubusercontent.com/oceanprotocol/art/master/github/repo-banner%402x.png)](https://oceanprotocol.com)

# mantaray

>    🐙 Data Science focused implementation of the Ocean Protocol stack and API for (Python).
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

Designed to be used with an interactive Python shell, for example the IPython
Read–Eval–Print Loop (REPL) found in [Jupyter Notebooks](http://jupyter.org/)
and other editors.

This repo is the source for the front-end facing notebooks. Here's a high level overview; 
1. First, scripts are written and tested here in this repo, using the `%%` format to deliniate code cells. Testing is done against local components (see the [barge](https://github.com/oceanprotocol/barge) project) or the deployed endpoints in AWS kubernetes. 
1. Next, the [jupytext](https://github.com/mwouts/jupytext) parser is used to create .ipynb notebooks. 
1. These notebooks are manually copied into a new [front-facing repo](https://github.com/oceanprotocol/mantaray_jupyter). It is this repo that is pulled into each JupyterLab instance, to keep things clean and simple for the end user. 
1. The [jupyterhub-helm-configuration](https://github.com/oceanprotocol/jupyterhub-helm-configuration) repo controls the creation of jupyterlab instances (using a [JupyterHub](https://jupyter.org/hub) cluster). 
1. A docker image of [jupyterhub-helm-configuration](https://github.com/oceanprotocol/jupyterhub-helm-configuration) is created and controls the git-pull of the notebooks, as well as any environment configuration (installation of all dependencies). (See the `Dockerfile` and the `post-start.sh` script in this repo for details.)
1. Now, for each user, a new container is instantiated (essentially a dedicated virtual machine) from the Dockerfile. The post-start script then pulls the latest notebooks and makes any other changes. 

One consequence of the above flow is that once the container and connected disk image are created, they cannot be automatically updated to new versions. 

## Installation

The primary use of Mantaray is an easy way to get starting with Ocean Protocol. Visit [datascience.oceanprotocol.com](https://datascience.oceanprotocol.com/) to test these scripts in a pre-configured Jupyter Lab environment! 

For developers seeking to work on scripts, see [this guide](doc/installation.md) for local development installation. 

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
