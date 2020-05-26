"""
This is a basic example of how to use the library to create a boxplot in Python
"""
from graphy2.core import Graphy
from graphy2.style_sheets import BLUE_ON_WHITE_GRID
import seaborn as sns
import os

if __name__ == "__main__":

    # Load an example dataset from seaborn as the sample dataset
    data = sns.load_dataset("tips")

    # Get the path for the directory of this file, and save output to new sub-directory 'plots'
    write_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "plots")

    # Modify a default style to have a smaller image size for a Non-print online only figure
    BLUE_ON_WHITE_GRID["dpi"] = 72

    # Call graphy2 to produce a box plot
    Graphy(data, write_dir, "Box Plot", BLUE_ON_WHITE_GRID).box_plot(x_var="day", y_var="total_bill")
