from setuptools import setup, find_packages

setup(
    name='plasticity',
    packages=find_packages(exclude=['tests', 'tests.*']),
    version='0.0.3',
    description='A Python package for the Plasticity API.',
    author='Plasticity',
    author_email='opensource@plasticity.ai',
    url='https://github.com/plasticityai/plasticity-python',
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
