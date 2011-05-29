#! /usr/bin/env python
from setuptools import setup
import sys, os

setup(
  name                 = 'js2coffee',
  version              = '0.1',
  description          = "JavaScript to CoffeeScript compiler",
  packages             = ['js2coffee'],
  include_package_data = True,
  zip_safe             = False,
  test_suite           = 'test',
  entry_points         = {
    'console_scripts': [
      'js2c = j2coffee:Main'
    ]
  }
  )

