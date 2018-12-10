#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

print("*** Packages ***")
packages = find_packages(include=['mantaray_utilities'])
for p in packages:
    print(p)
# for d, _, _ in os.walk('squid_py'):
#     if os.path.exists(join(d, '__init__.py')):
#         packages.append(d.replace(os.path.sep, '.'))
print()

setup(
    name='mantaray_utilities',
    author="leucothia",
    version='0.0.1',
    author_email='devops@oceanprotocol.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    description="Utilities sub-package for mantaray",
    packages=packages,
)
