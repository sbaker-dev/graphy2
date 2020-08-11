from graphy2.StyleSheet import StyleSheet
import os
import pandas as pd
import sys


class Common(StyleSheet):
    def __init__(self, write_directory, file_name):
        super().__init__()
        self._write_path = self._set_write_path(write_directory, file_name)

    def _set_style_sheet(self, new_style):
        """
        This takes an dict which is compared against the values set in the stylesheet, if a match is found then the
        stylesheet is updated with the new value
        :param new_style: style_sheet dictionary of keys and values to overide in class StyleSheet
        :type new_style: dict
        :return: Nothing, setattr all values for matching keys then end
        :rtype: None
        """
        # TODO This is not efficient and needs upgrading

        key_list, value_list = self.style_sheet
        for key, value in zip(key_list, value_list):
            for new_key in new_style:
                if new_key == key:
                    setattr(self, str(key), new_style[new_key])

    @staticmethod
    def _set_data_frame(data):
        """
        If the loaded data is not an instance of pandas dataframe, create one from the file type using pandas
        """
        if not isinstance(data, pd.Dataframe):
            file_type = data.split(".")[-1]

            if file_type == "csv":
                data = pd.read_csv(data)
            elif file_type == "xlsx":
                data = pd.read_excel(data)
            elif file_type == "dta":
                data = pd.read_stata(data)
            elif file_type == "sav":
                data = pd.read_spss(data)
            else:
                sys.exit(
                    "Error: File type not supported\nCurrent supported files are pandas.Dataframe, csv, xlsx,"
                    " dta and sav"
                )
        return data

    @staticmethod
    def _set_write_path(write_directory, file_name):
        """
        Construct the write path, insuring not to overwrite a file if it already exists within the directory
        """
        if os.path.isfile(os.path.join(write_directory, file_name + ".png")):
            length = len([file for file in os.listdir(write_directory)])
            return os.path.join(write_directory, file_name + str(length) + ".png")
        else:
            return os.path.join(write_directory, file_name + ".png")

    def write_plot(self, plot):
        """
        Writes out plot to .png to requested location.
        """

        try:
            plot.get_figure().savefig(self._write_path, bbox_inches="tight", dpi=self.dpi)

        except AttributeError:
            plot.savefig(self._write_path, dpi=self.dpi, bbox="tight")

        except (FileNotFoundError, OSError) as ex:
            # If any other errors are raised, print them to the console
            print(ex)

