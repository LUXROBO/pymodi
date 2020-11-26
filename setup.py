from os import path
from io import open
from setuptools import setup, find_packages


def get_spec(filename: str, mode: str = 'r'):
    def wrapper():
        here = path.dirname(__file__)
        result = {}
        with open(path.join(here, filename), encoding='utf8') as src_file:
            if mode == 'd':
                exec(src_file.read(), result)
            else:
                result = src_file.read()
        return result
    return wrapper


get_about = get_spec('./modi/about.py', 'd')
get_readme = get_spec('README.md')
get_history = get_spec('HISTORY.md')
get_requirements = get_spec('requirements.txt')
get_requirements_dev = get_spec('requirements-dev.txt')

about = get_about()
setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__email__'],
    description=about['__summary__'],
    long_description=get_readme() + '\n' + get_history(),
    long_description_content_type='text/markdown',
    install_requires=get_requirements(),
    extras_require={'dev': get_requirements_dev()},
    license=about['__license__'],
    include_package_data=True,
    keywords=['python', 'modi'],
    packages=find_packages(
        include=[
            'modi', 'modi.util', 'modi.task', 'modi.task.ble_task',
            'modi.module',
            'modi.module.setup_module',
            'modi.module.input_module',
            'modi.module.output_module'
        ]
    ),
    test_suite='tests',
    url=about['__url__'],
    classifiers=[
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
