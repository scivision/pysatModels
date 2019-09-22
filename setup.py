#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019, RS
# Full license can be found in License.md
# -----------------------------------------------------------------------------

import os
from codecs import open
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'description.txt'), encoding='utf-8') as f:
    long_description = f.read()
version_filename = os.path.join('pysatModelUtils', 'version.txt')
with open(os.path.join(here, version_filename)) as version_file:
    version = version_file.read().strip()

# change setup.py for readthedocs - commented for now
# on_rtd = os.environ.get('READTHEDOCS') == 'True'
install_requires = ['pysat']

# Run setup

setup(name='pysatModelUtils',
      version=version,
      url='github.com/pysat/pysatModelUtils',
      author='Angeline G. Burrell, Russell Stoneback',
      author_email='angeline.burrell@nrl.navy.mil',
      description='Model-data comparisons for the pysat ecosystem',
      long_description=long_description,
      packages=find_packages(),
      classifiers=[
          "Development Status :: 4 - Beta",
          "Topic :: Scientific/Engineering :: Physics",
          "Intended Audience :: Science/Research",
          "License :: BSD",
          "Natural Language :: English",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Operating System :: MacOS :: MacOS X",
      ],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      )
