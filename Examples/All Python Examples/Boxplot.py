"""
This is a basic example of how to use the library to create a boxplot in Python
"""
from graphy2.core import Graphy
from graphy2.StyleSheet import BLUE_ON_WHITE_GRID
import seaborn as sns

if __name__ == "__main__":

    # Load an example dataset from seaborn as the sample dataset
    data = sns.load_dataset("tips")

    # Modify a default style to have a smaller image size for a Non-print online only figure
    BLUE_ON_WHITE_GRID["dpi"] = 72

    # Call graphy2 to produce a box plot
    Graphy(data, "Box Plot", BLUE_ON_WHITE_GRID).box_plot(x_var="day", y_var="total_bill")
