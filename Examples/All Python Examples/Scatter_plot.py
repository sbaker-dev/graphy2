"""
This is a basic example of how to use the library natively in python.
"""
from graphy2.core import Graphy
import os
import seaborn as sns
from graphy2.style_sheets import COOL_ON_WHITE

if __name__ == "__main__":

    # Load data set
    diamonds = sns.load_dataset("diamonds")

    # Get the path for the directory of this file, and save output to new sub-directory 'plots'
    write_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "plots")

    # Use a custom ranking relating to the clarity within the data
    clarity_ranking = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]

    # Modify a prebuilt style to have a wider graph
    COOL_ON_WHITE["figure_x"] = 8

    # # Call graphy2 to produce the scatter plot
    Graphy(diamonds, write_dir, "Scatter Plot", COOL_ON_WHITE).scatter_plot("carat", "price", "clarity", "depth",
                                                                            clarity_ranking)
