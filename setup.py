#! /usr/bin/env python
from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
  name                 = 'js2coffee',
  version              = version,
  description          = "JavaScript to CoffeeScript compiler",
  packages             = find_packages(exclude = ['test']),
  include_package_data = True,
  zip_safe             = False,
  test_suite           = 'test',
  entry_points         = {
    'console_scripts': [
      'js2c = j2coffee:Main'
    ]
  }
  )

