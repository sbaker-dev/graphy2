"""
This is a basic example of how to use the library to create a lineplot in Python
"""
from graphy2.core import Graphy
import seaborn as sns

if __name__ == "__main__":

    # Load an example dataset from seaborn as the sample dataset
    data = sns.load_dataset("fmri")

    # Call graphy2 to produce a line plot
    Graphy(data, "Line Plot").line_plot(x_var="timepoint", y_var="signal")
