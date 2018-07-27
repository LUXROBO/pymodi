#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

import sys
IS_PY2 = sys.version_info < (3, 0)

if IS_PY2:
    requirements = ['pyserial>=3.1.1', 'enum34>=1.1.6', ]
else:
    requirements = ['pyserial>=3.1.1', ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Jinsoo Heo",
    author_email='koriel@luxrobo.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='modi',
    name='modi',
    packages=find_packages(include=['modi', 'modi.module']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/LUXROBO/MODI-Python-API',
    version='0.2.1',
    zip_safe=False,
)
