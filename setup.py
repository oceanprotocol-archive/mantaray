#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()

# Core requirements for end-users
requirements = [
    'squid-py==0.2.22'
]

# Required packages for developers
dev_requirements = [
    'jupytext==0.8.5', # For conversion of IPython scripts to Jupyter
    'bumpversion',
    #'pkginfo',
    'twine',
    #'watchdog',
]

# Extra requirements for setup
setup_requirements = []

# Requirements for testing
test_requirements = [
    'tox',
    'pytest',
]

docs_requirements = [
    'Sphinx',
    'sphinx-rtd-theme',
]

setup(
    author="leucothia",
    author_email='devops@oceanprotocol.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    description="Data Science interface to the Ocean Protocol stack",
    extras_require={
        'test': test_requirements,
        'dev': dev_requirements + test_requirements + docs_requirements,
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='mantaray',
    name='mantaray',
    packages=find_packages(include=['mantaray']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/oceanprotocol/mantaray',
    version='0.0.1',
    zip_safe=False,
)
