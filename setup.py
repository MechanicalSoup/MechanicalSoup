from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='MechanicalSoup',

    version='0.0.2',

    description='A Python library for automating interaction with websites',

    url='https://github.com/matt-hickford/MechanicalSoup',

    author='Matt Hickford',
    author_email='matt.hickford@gmail.com',

    license='MIT',

    classifiers=[
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    packages=['mechanicalsoup'],

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/technical.html#install-requires-vs-requirements-files
    install_requires=['requests', 'beautifulsoup4', 'six'],
)
