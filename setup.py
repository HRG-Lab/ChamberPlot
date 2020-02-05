# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='chamberplot',
    version='0.1.0',
    description='Package to read and plot the myriad of data types output from DAMS',
    long_description=readme,
    author='Bailey Campbell',
    author_email='baileycampbell1990@gmail.com',
    url='https://github.com/HRG-Lab/chamberPlot',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

