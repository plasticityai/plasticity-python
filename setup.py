from setuptools import setup, find_packages

setup(
    name = 'plasticity',
    version = '0.1',
    description = 'A Python package for the Plasticity API.',
    author = 'Plasticity',
    author_email = 'support@plasticity.ai',
    url = 'http://plasticity.ai/api',
    keywords = ["plasticity","nlp"],
    license = 'MIT',
    extras_require = {
        ':python_version<"3.0"': [
            "requests[security]",
        ],
        ':python_version>="3.0"': [
            "requests",
        ],
    },
    packages = find_packages(exclude=['tests', 'tests.*']),
    zip_safe = False
)