from graphy2 import pd, plt, sns, sys
from graphy2.styles import StyleSheet


class Graphy(StyleSheet):
    def __init__(self, data, write_directory, figure_name="Graphy_Output", style_sheet=None):
        super().__init__()

        if style_sheet:
            self._set_style_sheet(style_sheet)

        self._data = self._set_data_frame(data)
        self._write_directory = write_directory
        self._figure_name = figure_name

    def scatter_plot(self, x_variable, y_variable, gradient_variable=None, size_variable=None, custom_ranking=None):
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

        self._validate_variable_args(locals(), locals().values(), ['custom_ranking'])

        figure, axis = plt.subplots(figsize=(self.figure_x, self.figure_y))
        sns.despine(figure, left=True, bottom=True)
        plot = sns.scatterplot(x=x_variable, y=y_variable, data=self._data, palette=self.palette, ax=axis,
                               hue=gradient_variable, size=size_variable, hue_order=custom_ranking,
                               linewidth=self.outline_width, sizes=(self.min_point_size, self.max_point_size))
        plot.get_figure().savefig(f"{self._write_directory}/{self._figure_name}.png")
        return plot

    # def bar_plot(self, x_var, y_var, custm_hue, col_names, custom_data, kind = "bar", height_var, aspect_var):
    #     #bar plot with FacetGrid
    #     figure, axis = plt.subplots(figsize=(self.figure_x, self.figure_y))
    #     sns.despine(figure, left=True, bottom=True)
    #     plot = sns.catplot(x= x_var, y= y_var, hue=custm_hue,
    #                        col= col_names, data= custom_data,
    #                        kind=kind, height=height_var, aspect=aspect_var)
    #     plot.get_figure().savefig(f"{self._write_directory}/{self._figure_name}.png")
    #     return plot

    def kde_plot(self, x_var, y_var, cbar_var):
        figure, axis = plt.subplots(figsize=(self.figure_x, self.figure_y))
        sns.despine(figure, left=True, bottom=True)
        plot = sns.kdeplot(x=x_var, y=y_var, cbar=cbar_var)
        plot.get_figure().savefig(f"{self._write_directory}/{self._figure_name}.png")
        return plot

    def violin_plot(self, x_var, y_var, custom_hue, custom_data, custom_palette, if_split, custom_scale, if_inner, if_scale_hue, custom_bw):
        figure, axis = plt.subplots(figsize=(self.figure_x, self.figure_y))
        sns.despine(figure, left=True, bottom=True)
        plot = sns.violinplot(x=x_var, y=y_var, hue=custom_hue, data=custom_data,
                              palette=custom_palette, split=if_split, scale=custom_scale,
                              inner=if_inner, scale_hue= if_scale_hue, bw=custom_bw)
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
                    sys.exit(f"ERROR: {key} == {value} which is not in the databases list of variables seen below:\n"
                             f"{self._data.columns.tolist()}")

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
                sys.exit("Error: File type not supported\nCurrent supported files are pandas.Dataframe, csv, xlsx, dta"
                         " and sav")
        return data