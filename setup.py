from __future__ import with_statement
from setuptools import setup, find_packages

import os

__version__ = None
script_dir = os.path.dirname(__file__)
with open(os.path.join(script_dir, 'plasticity/version.py')) as f:
    exec(f.read())

setup_requires = [
    'pytest-runner',
]

install_requires = [
    'six',
]

tests_require = [
    'pytest == 3.4.1',
]

extras_require = {
    ':python_version<"3.0"': [
        "requests[security] >= 2.0.0",
    ],
    ':python_version>="3.0"': [
        "requests >= 2.0.0",
    ],
    'test': tests_require,
}

setup(
    name='plasticity',
    packages=find_packages(exclude=['tests', 'tests.*']),
    version=__version__,
    description='A Python package for the Plasticity API.',
    author='Plasticity',
    author_email='opensource@plasticity.ai',
    url='https://github.com/Plasticity/plasticity-python',
    keywords=['plasticity', 'nlp', 'nlu', 'natural language'],
    license='MIT',
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Intended Audience :: Developers',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
