from setuptools import setup, find_packages


# To install the twilio-python library, open a Terminal shell, then run this
# file by typing:
#
# python setup.py install
#
# You need to have the setuptools module installed. Try reading the setuptools
# documentation: http://pypi.python.org/pypi/setuptools

setup(
    name='plasticity',
    packages=find_packages(exclude=['tests', 'tests.*']),
    version='0.0.1',
    description='A Python package for the Plasticity API.',
    author='Plasticity',
    author_email='support@plasticity.ai',
    url='https://gitlab.com/Plasticity/plasticity-python',
    keywords=['plasticity', 'nlp'],
    license='MIT',
    install_requires=[
        "six",
    ],
    extras_require={
        ':python_version<"3.0"': [
            "requests[security] >= 2.0.0",
        ],
        ':python_version>="3.0"': [
            "requests >= 2.0.0",
        ],
    },
)
