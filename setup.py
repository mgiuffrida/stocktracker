#!/usr/bin/env python2

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='stocktracker',
    version='0.0.1',
    description='stocktracker',
    long_description=readme,
    author='Michael Giuffrida',
    author_email='michaelg@michaelg.us',
    url='https://github.com/mgiuffrida/stocktracker',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
