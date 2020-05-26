// load some data
use "C:\Path\To\File.dta"

// Do some analysis here

// Save the data file out
save "C:\Path\To\File.dta", replace


// Initialise python
python

// Then its the same as basic_python example
from graphy2.core import Graphy

csv_path = r"C:\Path\To\File.dta"
write_dir = r"C:\Directory\To\Save\To"

clarity_ranking = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]

Graphy(csv_path, write_dir, "Stata_figure").scatter_plot(
"carat", "price", "clarity", "depth")

end