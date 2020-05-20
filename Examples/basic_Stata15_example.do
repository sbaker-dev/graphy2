clear all
use "C:\Users\Samuel\Pictures\Graphy\Diamonds.dta"

// Do some analaysis here

local data_path "C:\Users\Samuel\Pictures\Graphy\Diamonds.dta"

// Save the data file out
save `data_path', replace

// Now you need to set the path to the graphy2\api.py file as non stata 16 
// versions do not have python nativly.
local python_path "C:\Users\Samuel\PycharmProjects\Grapher\graphy2\api.py" 

// You can then run Graphy, in this case with less arguments. Check the help
// files for the graph in question to get args list and order
graphy2_scatter `python_path' `data_path' carat price clarity depth