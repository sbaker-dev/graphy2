"""
This is a basic example of how to use the library to create a kdeplot in Python
"""
from graphy2.core import Graphy
import numpy as np; np.random.seed(10)
import pandas as pd
if __name__ == "__main__":

    import seaborn as sns
    import os

    # Load an example dataset from seaborn as the sample dataset
    mean, cov = [0, 2], [(1, .5), (.5, 1)]
    x, y = np.random.multivariate_normal(mean, cov, size=50).T
    data = pd.DataFrame({'X': x, 'Y':y}, columns = ['X', 'Y'])

    # Get the path for the directory of this file, and save output to new sub-directory 'plots'
    write_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "plots")

    # Call graphy2 to produce a box plot
    Graphy(data, write_dir).kde_plot()
