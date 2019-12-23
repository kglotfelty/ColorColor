#!/usr/bin/env python


import os
import sys

assert "ASCDS_INSTALL" in os.environ


from distutils.core import setup

"""
python setup.py build --force -e '/usr/bin/env python' \
  install --prefix=$ASCDS_INSTALL/contrib --force
"""


setup( name='color_color',
        version='0.0.1',
        description='CIAO color color (hardness ratio) diagram',
        author='Anonymous',
        author_email='glotfeltyk@si.edu',
        url='https://github.com/kglotfelty/ColorColor/',
        py_modules=["color_color",],
        scripts = ["color_color",],
        data_files = [ ("param", ["color_color.par",])]
        )
