from graphy2 import pd, plt, sns, sys
from graphy2.styles import StyleSheet


class Graphy(StyleSheet):
    def __init__(
        self, data, write_directory, figure_name="Graphy_Output", style_sheet=None
    ):
        super().__init__()

        if style_sheet:
            self._set_style_sheet(style_sheet)

        self._data = self._set_data_frame(data)
        self._write_directory = write_directory
        self._figure_name = figure_name

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
        figure, axis = plt.subplots(figsize=(self.figure_x, self.figure_y))
        sns.despine(figure, left=True, bottom=True)
        plot = sns.scatterplot(
            x=x_variable,
            y=y_variable,
            data=self._data,
            palette=self.palette,
            ax=axis,
            hue=gradient_variable,
            size=size_variable,
            hue_order=custom_ranking,
            linewidth=self.outline_width,
            sizes=(self.min_point_size, self.max_point_size),
        )
        plot.get_figure().savefig(f"{self._write_directory}/{self._figure_name}.png")
        return plot

    def box_plot(
        self,
        x_var,
        y_var,
        gradient_variable=None,
        custom_ranking=None,
        orientation=None,
    ):
        """Create a box plot in seaborn using the style sheet and chosen variable values. 

        Arguments:
            x_var -- x-axis variable name
            y_var -- y-axis variable name

        Keyword Arguments:
            gradient_variable -- A variable to apply a gradient of colour to the points (default: {None})
            custom_ranking {list}-- A list of rankings to use instead of the default set (default: {None})
            orientation {“v” | “h”} -- Whether the plot should be vertical or horizontal (default: {None})

        Returns:
            plot {matplotlib subplot object} -- The plot is returned, and .png saved to the write directory
        """

        # Validate the arguments provided
        self._validate_variable_args(
            locals(), locals().values(), ["custom_ranking", "orientation"]
        )

        # Set defaults before plotting
        figure, axis = plt.subplots(figsize=(self.figure_x, self.figure_y))
        sns.despine(figure, left=True, bottom=True)

        # Generate the plot
        # NB Some arguments are left at default that are given sensible defaults by seaborn
        plot = sns.boxplot(
            x=x_var,
            y=y_var,
            data=self._data,
            palette=self.palette,
            linewidth=self.outline_width,
            hue=gradient_variable,
            orient=orientation,
            hue_order=custom_ranking,
            order=custom_ranking,
            ax=axis,
        )

        # Write out the plot to chosen write directory as a png
        plot.get_figure().savefig(f"{self._write_directory}/{self._figure_name}.png")

        return plot

    def line_plot(
        self,
        x_var,
        y_var,
        gradient_variable=None,
        size_variable=None,
        custom_ranking=None,
    ):
        """Create a line plot in seaborn using the style sheet and chosen variable values.

        Arguments:
            x_var -- x-axis variable name
            y_var -- y-axis variable name

        Keyword Arguments:
            gradient_variable -- Name of variable to apply a gradient of colour to the points (default: {None})
            size_variable {str} -- Name of the variable that decides line width (default: {None})
            custom_ranking {list} -- A list of rankings to use instead of the default set (default: {None})

        Returns:
            plot {matplotlib subplot object} -- The plot is returned, and .png saved to the write directory
        """

        # Validate the arguments provided
        self._validate_variable_args(locals(), locals().values(), ["custom_ranking"])

        # Set defaults before plotting
        figure, axis = plt.subplots(figsize=(self.figure_x, self.figure_y))
        sns.despine(figure, left=True, bottom=True)

        # Generate the plot
        # NB Some arguments are left at default that are given sensible defaults by seaborn
        plot = sns.lineplot(
            x=x_var,
            y=y_var,
            data=self._data,
            hue=gradient_variable,
            size=size_variable,
            palette=self.palette,
            hue_order=custom_ranking,
            sizes=(self.min_point_size, self.max_point_size),
            ax=axis,
        )

        # Write out the plot to chosen write directory as a png
        plot.get_figure().savefig(f"{self._write_directory}/{self._figure_name}.png")

        return plot

    def residual_plot(
        self, x_var, y_var, ignore_na=True, colour=None, legend_label=None
    ):
        """Regress y_var on x_var, and then draw a scatterplot of the residuals.

        Arguments:
            x_var -- x-axis variable name
            y_var -- y-axis variable name

        Keyword Arguments:
            ignore_na {bool} -- If True, ignore observations with missing data when fitting and plotting (default: {True})
            colour {matplotlib color} -- Colour to use for all elements of the plot (default: {None})
            legend_label {str} -- Label that will be used in any plot legends (default: {None})

        Returns:
            plot {matplotlib subplot object} -- The plot is returned, and .png saved to the write directory
        """
        # Validate the arguments provided
        self._validate_variable_args(
            locals(), locals().values(), ["ignore_na", "colour", "legend_label"]
        )

        # Set defaults before plotting
        figure, axis = plt.subplots(figsize=(self.figure_x, self.figure_y))
        sns.despine(figure, left=True, bottom=True)

        # Generate the plot
        # NB Some arguments are left at default that are given sensible defaults by seaborn
        plot = sns.residplot(
            x=x_var,
            y=y_var,
            data=self._data,
            dropna=ignore_na,
            label=legend_label,
            color=colour,
            ax=axis,
        )

        # Write out the plot to chosen write directory as a png
        plot.get_figure().savefig(f"{self._write_directory}/{self._figure_name}.png")

        return plot

    def _set_style_sheet(self, new_style):
        """
        This takes an dict which is compared against the values set in the stylesheet, if a match is found then the
        stylesheet is updated with the new value
        :param new_style: style_sheet dictionary of keys and values to overide in class StyleSheet
        :type new_style: dict
        :return: Nothing, setattr all values for matching keys then end
        :rtype:None
        """
        key_list, value_list = self.style_sheet
        for key, value in zip(key_list, value_list):
            for new_key in new_style:
                if new_key == key:
                    setattr(self, str(key), new_style[new_key])

    def _validate_variable_args(self, local_args, local_arg_values, exemption_list):
        """
        A method to validate that all the args that need to be a column header name do exist within the column names
        :param local_args: The args of the current method
        :type local_args: dict
        :param local_arg_values: The values of the args of the current method
        :type local_arg_values: values.view
        :param exemption_list: Key values to be ignored
        :type exemption_list: list
        :return: Nothing, simply check all args that need checking are within the column names
        :rtype: None
        """

        for key, value in zip(local_args, local_arg_values):
            if value and key != "self" and key not in exemption_list:
                if value not in self._data.columns.tolist():
                    sys.exit(
                        f"ERROR: {key} == {value} which is not in the databases list of variables seen below:\n"
                        f"{self._data.columns.tolist()}"
                    )

    @staticmethod
    def _set_data_frame(data):
        """
        If the loaded data is not an instance of pandas dataframe, create one from the file type using pandas
        :param data: data to be verified and if need be loaded
        :type: Any
        :return: An instance of pandas data frame
        :rtype: pandas.core.frame.DataFrame
        """

        if not isinstance(data, pd.DataFrame):
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
                    "Error: File type not supported\nCurrent supported files are pandas.Dataframe, csv, xlsx, dta"
                    " and sav"
                )
        return data
