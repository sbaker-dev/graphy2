#! /usr/bin/env python
# Copyright (C) 2020 Samuel Baker, Nina Di Cara, Oliwia Michalak

DESCRIPTION = "graphy: cross platform compatible graphs and tables"
LONG_DESCRIPTION = """"/graphy is designed to try and insure that a given table or graph standard can be constructed 
from any given statistical or python platform. It is built on top of many external libraries listed below and acts as 
an API for these libraries. The core libraries graphy is currently using are:
 
 Seaborn:       <https://github.com/mwaskom/seaborn>
 Pandas:        <https://github.com/pandas-dev/pandas>
 matplotlib:    <https://github.com/pandas-dev/pandas>
 
 graphy can be called within python but graphy also comes with a wrapper for R, Stata and SPSS so that individuals can 
 still use the program from the software/code type they prefer. It is designed to be as simple as possible, with most
 commands being pushed to a single line. graphy also contains a list of styles for well used graphs/tables that should
 reflect the standards expected from certain journals.
  /"""

 
DISTNAME = 'graphy'
MAINTAINER = 'Samuel Baker, Nina Di Cara, Oliwia Michalak'
MAINTAINER_EMAIL = 'samuelbaker.researcher@gmail.com'
LICENSE = 'MIT'
DOWNLOAD_URL = "https://github.com/samuelbaker93/graphy"
VERSION = "0.02.0"
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
    "graphy",
]

CLASSIFIERS = [
    'Intended Audience :: Science/Research/Statistics',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'License :: MIT',
    'Topic :: Multimedia :: Graphics',
    'Operating System :: Windows',
]

if __name__ == "__main__":

    from setuptools import setup

    import sys
    if sys.version_info[:2] < (3, 7):
        raise RuntimeError("graphy requires python >= 3.7.")

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