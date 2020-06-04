from os import path
from setuptools import setup, find_packages


def get_readme():
    here = path.dirname(__file__)
    with open(path.join(here, 'README.md'), encoding='UTF8') as readme_file:
        readme = readme_file.read()
        return readme


def get_about():
    here = path.dirname(__file__)
    about = {}
    with open(path.join(here, './modi/about.py'),
              encoding='UTF8') as about_file:
        exec(about_file.read(), about)
        return about


about = get_about()


def get_history():
    here = path.dirname(__file__)
    with open(path.join(here, 'HISTORY.md'), encoding='UTF8') as history_file:
        history = history_file.read()
        return history


def get_requirements():
    here = path.dirname(__file__)
    with open(path.join(here, 'requirements.txt'),
              encoding='UTF8') as requirements_file:
        requirements = requirements_file.read().splitlines()
        return requirements


setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__email__'],
    description=about['__summary__'],
    long_description=get_readme() + '\n' + get_history(),
    long_description_content_type="text/markdown",
    install_requires=get_requirements(),
    license=about['__license__'],
    include_package_data=True,
    keywords=["pymodi", "modi", "luxrobo"],
    packages=find_packages(include=['modi', 'modi.util', 'modi.task',
                                    'modi.module',
                                    'modi.module.setup_module',
                                    'modi.module.input_module',
                                    'modi.module.output_module']),
    test_suite="tests",
    url=about['__url__'],
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)
