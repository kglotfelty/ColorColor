#!/usr/bin/env python


# For ciao installed using ciao-install:
#
#     python setup.py build -e "/usr/bin/env python" install --prefix "$ASCDS_INSTALL/contrib" 
#
# For ciao installed using conda
#
#     python setup.py install


import os
import sys

assert "ASCDS_INSTALL" in os.environ, "Please setup for CIAO before installing"

from setuptools import setup
from setuptools.command.install import install


class InstallAhelpWrapper(install):
    'A simple wrapper to run ahelp -r after install to update ahelp index'

    @staticmethod
    def update_ahelp_database():
        print("Update ahelp database ...")
        from subprocess import check_output
        sout = check_output(["ahelp","-r"])
        for line in sout.decode().split("\n"):
            for summary in ["Processed", "Succeeded", "Failed", "Purged"]:
                if line.startswith(summary):
                    print("    "+line)

    
    def run(self):
        install.run(self)
        self.update_ahelp_database()



setup( name='color_color',
        version='4.13.0',
        description='CIAO color color (hardness ratio) diagram',
        author='Kenny Glotfelty',
        author_email='glotfeltyk@si.edu',
        url='https://github.com/kglotfelty/ColorColor/',
        py_modules=["color_color",],
        scripts = ["color_color",],
        data_files = [ ("param", ["color_color.par",]),        
                       ('share/doc/xml',['color_color.xml',])
                     ],
        cmdclass={'install': InstallAhelpWrapper},
        )
