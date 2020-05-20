#! /usr/bin/env python
# Copyright (C) 2020 Samuel Baker, Nina Di Cara, Oliwia Michalak

DESCRIPTION = "graphy2: cross platform compatible graphs and tables"
LONG_DESCRIPTION = """
graphy2 is designed to try and insure that a given table or graph standard can be constructed 
from any given statistical or python platform. It is built on top of many external libraries listed below and acts as 
an API for these libraries. The core libraries graphy2 is currently using are:
 
Seaborn:       <https://github.com/mwaskom/seaborn>  
Pandas:        <https://github.com/pandas-dev/pandas>  
matplotlib:    <https://github.com/pandas-dev/pandas>  
 
graphy2 can be called within python but graphy2 also comes with a wrapper for Rgraphy2, Stata and SPSS so that individuals can 
still use the program from the software/code type they prefer. It is designed to be as simple as possible, with most
commands being pushed to a single line. graphy2 also contains a list of styles for well used graphs/tables that should
reflect the standards expected from certain journals.
"""

DISTNAME = 'graphy2'
MAINTAINER = 'Samuel Baker, Nina Di Cara, Oliwia Michalak'
MAINTAINER_EMAIL = 'samuelbaker.researcher@gmail.com'
LICENSE = 'MIT'
DOWNLOAD_URL = "https://github.com/sbaker-dev/graphy2"
VERSION = "0.02.3"
PYTHON_REQUIRES = ">=3.6"

INSTALL_REQUIRES = [
    "seaborn>=0.10.1",
    "pandas>=1.0.3",
    "matplotlib>=3.2.1",
    "cycler>=0.10.0",
    "kiwisolver>=1.2.0",
    "pyparsing>=2.4.7",
    "python-dateutil>=2.8.1",
    "pytz>=2020.1",
]


PACKAGES = [
    "graphy2",
]

CLASSIFIERS = [
    'Intended Audience :: Science/Research',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'License :: OSI Approved :: MIT License',
    'Topic :: Multimedia :: Graphics',
    'Operating System :: Microsoft :: Windows :: Windows 10'
]

if __name__ == "__main__":

    from setuptools import setup

    import sys
    if sys.version_info[:2] < (3, 7):
        raise RuntimeError("graphy2 requires python >= 3.7.")

    setup(
        name=DISTNAME,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license=LICENSE,
        version=VERSION,
        download_url=DOWNLOAD_URL,
        python_requires=PYTHON_REQUIRES,
        install_requires=INSTALL_REQUIRES,
        packages=PACKAGES,
        classifiers=CLASSIFIERS
    )