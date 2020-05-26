"""
This is a basic example of how to use the library natively in python.
"""
from graphy2.core import Graphy

if __name__ == "__main__":
    write_dir = r"C:\Users\Samuel\Pictures\Graphy"
    stylesheet = {"figure_x": 10}
    csv_path = r"C:\Users\Samuel\Pictures\Graphy\Diamonds.csv"

    clarity_ranking = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]

    Graphy(csv_path, write_dir).scatter_plot("carat", "price", "clarity", "depth")
