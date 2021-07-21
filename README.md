### Legacy

This package has been set to legacy due to it being easier to remake the figures to be fully customisable via 
subprocess of Blender than dealing with multiple different sub packages. Blender and python are cross-platform, allowing
for this to be easiest and most modular way of creating different types of the same figures. You can find the working
package for this at [pyBlendFigure](https://github.com/sbaker-dev/pyBlendFigures)

###### graphy2
graphy2: cross platform compatible graphs and tables

graphy2 is designed to try and insure that a given table or graph standard can be constructed 
from any given statistical or python platform. It is built on top of many external libraries listed below and acts as 
an API for these libraries. The core libraries graphy2 is currently using are:
 
 Seaborn:       <https://github.com/mwaskom/seaborn>  <br />
 Pandas:        <https://github.com/pandas-dev/pandas>  <br />
 matplotlib:    <https://github.com/pandas-dev/pandas>  <br />
 
 graphy2 can be called within python but graphy2 also comes with a wrapper for R, Stata and SPSS so that individuals can 
 still use the program from the software/code type they prefer. It is designed to be as simple as possible, with most
 commands being pushed to a single line. graphy2 also contains a list of styles for well used graphs/tables that should
 reflect the standards expected from certain
