"""
This is a basic example of how to use the library natively in python.
"""
from graphy2.core import Graphy

if __name__ == "__main__":

    # Set the file path
    csv_path = "./Path/to/your/file.csv"

    # Set where to save your file
    write_dir = "./Save/Directory"

    # Call graphy2's Graphy for the graph you want
    Graphy(csv_path, write_dir).scatter_plot("carat", "price", "clarity", "depth")
