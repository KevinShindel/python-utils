""" script Setup.py for creating a whl file with the package."""

from setuptools import setup, find_packages

import os


def read_pipenv_dependencies(file_name: str = 'Pipfile.lock'):
    """ Retrieve from Pipfile.lock default requirements."""
    filepath = os.path.join(os.path.dirname(__file__), file_name)
    with open(filepath) as req_file:
        return req_file.read().splitlines()


if __name__ == '__main__':
    setup(
        name='demo',  # Name of the package
        version=os.getenv('PACKAGE_VERSION', '0.0.dev0'),  # Version of the package
        package_dir={'': 'src'},  # Directory where the package is located
        packages=find_packages('src', include=[  # Include all packages in the src directory
            'demo*'
        ]),
        description='A demo package.',  # Description of the package
        install_requires=[  # Install dependencies
            *read_pipenv_dependencies('requirements.txt'),
        ],
        test_suite='tests.demo',  # Test suite
        tests_require=[  # Test dependencies
            *read_pipenv_dependencies('requirements-dev.txt'),
        ],
    )
