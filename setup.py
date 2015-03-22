#!/usr/bin/env python

from os.path import exists
from setuptools import setup

setup(name="toolshed",
      version="0.0.1",
      description='Extension to toolz library.',
      url='http://github.com/justanr/toolshed',
      author='https://raw.github.com/justanr/toolshed/AUTHORS.md',
      maintainer='Alec Reiter',
      maintainer_email='alecreiter@gmail.com',
      license='BSD',
      keywords='functional utility itertools functools toolz',
      install_requires=['toolz'],
      packages=['toolshed'],
      package_data={'toolshed': ['tests/*.py']},
      long_description=(open('README.rst').read() if exists('README.rst')
                        else ''),
      zip_safe=False)
