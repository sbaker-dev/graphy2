// load some data
use "C:\Users\Samuel\Pictures\Graphy\Diamonds.dta" 

// Do some analaysis here

// Save the data file out
save "C:\Users\Samuel\Pictures\Graphy\Diamonds.dta", replace


// Initlaise python
python

// Then its the same as basic_python example
from graphy2.core import Graphy

csv_path = r"C:\Users\Samuel\Pictures\Graphy\Diamonds.dat"
write_dir = r"C:\Users\Samuel\Pictures\Graphy"

clarity_ranking = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]

Graphy(csv_path, write_dir, "Statafigure").scatter_plot(
"carat", "price", "clarity", "depth")

end