from graphy2.core import Graphy
import os
from pathlib import Path

def directory_iterator(directory, file_only=True):
    """
    This takes a directory and returns a list of entries within that directory, if file_only is selected only
    files as apposed to directories will be returned

    :param directory: The directory you wish to iterate through
    :type directory: str

    :param file_only: Defaults to true where the return is just a list of files
    :type file_only: bool

    :return: List of entries from the directory
    :rtype: list
    """

    if file_only:
        return [file for file in os.listdir(directory) if os.path.isfile(f"{directory}/{file}")]
    else:
        return [file for file in os.listdir(directory)]

if __name__ == '__main__':

    # read_data = r"C:\Users\Samuel\PycharmProjects\graphy2\ExampleData\Binary_meta_event_total.csv"

    read_data = r"C:\Users\Samuel\PycharmProjects\AsthmaDisease\Testing"

    for index, file in enumerate(directory_iterator(read_data)):
        print(file)
        a = Path(read_data, file)
        if a.suffix == ".csv":
            Graphy(f"{read_data}/{file}", f"A{index}").forest_plot()


    # Graphy(f"{read_data}/base_forest.csv", "scarlet").forest_plot()
    # Graphy(f"{read_data}/sc_cont.csv", "sc_cont").forest_plot()
    # Graphy(f"{read_data}/sc_scarlet.csv", "sc_scarlet").forest_plot()
    # Graphy(f"{read_data}/sci_cont.csv", "sci_cont").forest_plot()
    # Graphy(f"{read_data}/sci_scarlet.csv", "sci_scarlet").forest_plot()
    # Graphy(f"{read_data}/sci_int.csv", "sci_int").forest_plot()
    # Graphy(f"{read_data}/sr_risk.csv", "sr_risk").forest_plot()
    # Graphy(f"{read_data}/sr_scarlet.csv", "sr_scarlet").forest_plot()
    # Graphy(f"{read_data}/sri_int.csv", "sri_int").forest_plot()
    # Graphy(f"{read_data}/sri_scarlet.csv", "sri_scarlet").forest_plot()
    # Graphy(f"{read_data}/sri_risk.csv", "sri_risk").forest_plot()
    #
    # Graphy(f"{read_data}/.csv", "AVbase_Forest").forest_plot()
    # Graphy(f"{read_data}/AVsci_scarlet.csv", "AVsci_scarlet").forest_plot()
    # Graphy(f"{read_data}/AVsci_int.csv", "AVsci_int").forest_plot()
    #
    # Graphy(f"{read_data}/AVsri_scarlet.csv", "AVsri_scarlet").forest_plot()
    # Graphy(f"{read_data}/AVsri_int.csv", "AVsri_int").forest_plot()
    #








