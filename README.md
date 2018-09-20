[![banner](https://raw.githubusercontent.com/oceanprotocol/art/master/github/repo-banner%402x.png)](https://oceanprotocol.com)

# ocean-repo-name

>    🐳  [Data Science level 2 ](https://www.elastic.co/) production and management for (Python).
>    [oceanprotocol.com](https://oceanprotocol.com)

TODO Change this to match the repo name and testing environments
[![Travis (.com)](https://img.shields.io/travis/com/oceanprotocol/oceandb-elasticsearch-driver.svg)](https://travis-ci.com/oceanprotocol/oceandb-elasticsearch-driver)
[![Codacy coverage](https://img.shields.io/codacy/coverage/de067a9402c64b989c76b27cfc74fefe.svg)](https://app.codacy.com/project/ocean-protocol/oceandb-elasticsearch-driver/dashboard)
[![PyPI](https://img.shields.io/pypi/v/oceandb-elasticsearch-driver.svg)](https://pypi.org/project/oceandb-elasticsearch-driver/)
[![GitHub contributors](https://img.shields.io/github/contributors/oceanprotocol/oceandb-elasticsearch-driver.svg)](https://github.com/oceanprotocol/oceandb-elasticsearch-driver/graphs/contributors)

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

Manage assets for data science
 - Upload datasets and metadata for production testing
 -
 - Register assets into smart contracts
 -

## Prerequisites

### Create a new virtual environment
Using pip, conda, etc.

Activate the environment.
### Install the [osmosis-aws-driver](https://github.com/oceanprotocol/osmosis-aws-driver) S3 plugin to manage datasets on S3


Install the package itself, from local git repo, or online from Github;
`~/ocn/osmosis-aws-driver/pip install -e .`

`pip install git+https://github.com/tangentlabs/django-oscar-paypal.git@issue/34/oscar-0.6`


`conda env update --name mantaray1`

`keeper-contracts` running
## Quickstart

...


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
