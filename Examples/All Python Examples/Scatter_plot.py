"""
This is a basic example of how to use the library natively in python.
"""
from graphy2.core import Graphy
import seaborn as sns
from graphy2.StyleSheet import COOL_ON_WHITE

if __name__ == "__main__":
    # Load data set
    diamonds = sns.load_dataset("diamonds")

    # Use a custom ranking relating to the clarity within the data
    clarity_ranking = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]

    # Modify a prebuilt style to have a wider graph
    COOL_ON_WHITE["figure_x"] = 8

    # # Call graphy2 to produce the scatter plot
    Graphy(diamonds, "Scatter Plot", COOL_ON_WHITE).scatter_plot("carat", "price", "clarity", "depth", clarity_ranking)
