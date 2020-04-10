#!/usr/bin/env python

from setuptools import setup, find_packages

from os import path


def get_readme():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.md'), encoding='utf-8') as readme_file:
        readme = readme_file.read()
    return readme

def get_requirements():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'requirements.txt'), encoding='utf-8') as \
        requirements_file:
        requirements = requirements_file.read().splitlines()
        return requirements

setup(
    version="0.7.1",
    author="Jinsung Ha",
    author_email="jinsung@luxrobo.com",
    description="Easy😆 and fast💨 MODI Python API package.",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    install_requires=get_requirements(),
    license="MIT license",
    include_package_data=True,
    keywords=["pymodi", "modi", "luxrobo"],
    name="pymodi",
    packages=find_packages(include=['modi', 'modi.module',
                                    'modi.module.setup_module',
                                    'modi.module.input_module',
                                    'modi.module.output_module']),
    test_suite="tests",
    url="https://github.com/LUXROBO/pyMODI",
    classifiers=[
        "Natural Language :: English",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)
