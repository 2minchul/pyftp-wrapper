# -*- coding: utf-8 -*-
from setuptools import setup
import os

# Include __about__.py.
__dir__ = os.path.dirname(__file__)
about = {}
with open(os.path.join(__dir__, 'pyftp_wrapper', '__about__.py')) as f:
    exec(f.read(), about)

setup(
    name='pyftp_wrapper',
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    packages=['pyftp_wrapper'],
    install_requires=['pyftp==0.1.0'],

    url='http://github.com/2minchul/pyftp-wrapper',
    keywords='pyftp, python ftp',
    description='More high level ftp client wrapper based on pyftp.',
    platforms='any',
    license=about['__license__'],
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Topic :: Utilities',
    ],
)
