from graphy2.StyleSheet import StyleSheet
import os


class Common(StyleSheet):
    def __init__(self, write_directory, file_name):
        super().__init__()
        self._write_path = self._set_write_path(write_directory, file_name)

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

