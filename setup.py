# File: setup.py
# Coding: utf-8
# Author: Matteo Berchier (matteo.berchier@gmail.com)
# Package: pandatools

# --------------- Summary --------------- #
# Custom made tools to use with pandas data-frames

from setuptools import setup

setup(name='pandatools',
      version='0.0.1',
      description='Custom made tools to use with pandas data-frames',
      url='https://github.com/matteobe/pandas_tools.git',
      packages=[
          'pandatools'
      ],
      python_requires='>3.5.0',
      install_requires=[
          'numpy',
          'pandas'
      ],
      zip_safe=False)