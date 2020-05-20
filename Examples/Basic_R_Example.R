# Example Script
# This is designed to demo how to install and use Graphy2 within R

# You need devtools to use install_github. Given Graphy is not a core R repoistory, you need to use subdir
library(devtools)
install_github("sbaker-dev/graphy2", subdir = "Rgraphy2")

# Path to your python installation
python_path <- "C:/Users/Samuel/AppData/Local/Programs/Python/Python37"

# Relevent data paths
data_path <- "C:/Users/Samuel/Pictures/Graphy/Diamonds.csv"
write_dir <- "C:/Users/Samuel/Pictures/Graphy"

library(Rgraphy2)
Rgraphy2::scatterPlot(python_path, data_path, write_dir, "RFIGOUT", "carat", "price", "clarity", "depth")


