"""
This is a basic example of how to use the library to create a violinplot in Python
"""
from graphy2.core import Graphy

if __name__ == "__main__":

    import seaborn as sns
    import os

    # Load an example dataset from seaborn as the sample dataset
    data = sns.load_dataset("tips")

    # Get the path for the directory of this file, and save output to new sub-directory 'plots'
    write_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "plots")

    # Call graphy2 to produce a box plot
    Graphy(data, write_dir).violin_plot(x_var="day", y_var="total_bill",
                                        gradient_variable="sex", pal_var="Set2", split_var=True,
                                        scale_var="count", inner_var="stick", scale_gradiet=False)
