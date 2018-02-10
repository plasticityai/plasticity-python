from setuptools import setup, find_packages

setup(
    name='plasticity',
    packages=find_packages(exclude=['tests', 'tests.*']),
    version='0.0.2',
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
