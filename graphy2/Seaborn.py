from graphy2.StyleSheet import StyleSheet
from graphy2.Common import Common
import seaborn as sns
import sys
import os


class SeabornAPI(Common, StyleSheet):
    def __init__(self, data, file_name, style_sheet=None, write_directory="", ):
        super().__init__(write_directory=self._set_write_directory(write_directory), file_name=file_name)

        if style_sheet:
            self._set_style_sheet(style_sheet)

        self._data = self._set_data_frame(data)

    def scatter_plot(
        self,
        x_variable,
        y_variable,
        gradient_variable=None,
        size_variable=None,
        custom_ranking=None,
    ):
        """
        This creates a scatter plot from and x and y variable with the option to have gradient and size variation for
        each points. If you want to have a ranking different from base, please specify an ordered list to custom
        ranking

        :param x_variable: The variable you want on the x axis
        :type x_variable: str

        :param y_variable: The variable you want on the y axis
        :type y_variable: str

        :param gradient_variable: A variable to apply a gradient of colour to the points
        :type gradient_variable: str

        :param size_variable: A variable to vary the size of the points
        :type size_variable: str

        :param custom_ranking: A list of rankings to use instead of the default set
        :type custom_ranking: list

        :return: The seaborn plot is returned if users wish to do something with it, the figure is also saved to the
            write directory

        :rtype: matplotlib.axes._subplots.AxesSubplot
        """

        self._validate_variable_args(locals(), locals().values(), ["custom_ranking"])

        plot = sns.scatterplot(
            x=x_variable,
            y=y_variable,
            data=self._data,
            palette=self.palette(),
            ax=self.seaborn_figure(),
            hue=gradient_variable,
            size=size_variable,
            hue_order=custom_ranking,
            linewidth=self.outline_width,
            sizes=(self.min_point_size, self.max_point_size),
        )

        # Write out the plot to chosen write directory as a png
        self.write_plot(plot)

        return plot

    @staticmethod
    def _set_write_directory(write_directory):
        """
        If no directory is set, get the directory of the call file and the write sub-directory 'plots"

        :param write_directory: A path or string location to write the files produced to, defaults to an empty string
        :type write_directory: str | Path

        :return: A path to uses as the write directory
        """
        if write_directory == "":
            return os.path.join(os.getcwd(), "plots")
        else:
            return os.path.realpath(write_directory)

    def _validate_variable_args(self, local_args, local_arg_values, exemption_list):
        """
        A method to validate that all the args that need to be a column header name do exist within the column names
        """

        for key, value in zip(local_args, local_arg_values):
            if value and key != "self" and key not in exemption_list:
                if value not in self._data.columns.tolist():
                    sys.exit(
                        f"ERROR: {key} == {value} which is not in the databases list of variables seen below:\n"
                        f"{self._data.columns.tolist()}"
                    )