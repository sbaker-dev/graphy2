from graphy2 import pd, sns, sys
from graphy2.styles import StyleSheet
from pathlib import Path
from graphy2.data import Data
import os
import cv2
from matplotlib.image import imread as mat_imread
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Graphy(StyleSheet):
    def __init__(
        self, data, figure_name="Graphy_Output", style_sheet=None,  write_directory=""
    ):
        super().__init__()

        if style_sheet:
            self._set_style_sheet(style_sheet)

        self._data = self._set_data_frame(data)
        self._write_directory = self._set_write_directory(write_directory)
        self._figure_name = self._set_figure_name(figure_name)
        self._file_path = self._set_file_path()

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

    def forest_plot(self, weight_area=50):

        # todo currently hard coded for odds
        df = Data(self._data).odds_ratio()
        #
        # # todo This produces a super rough table that needs formatting
        fig, axis = StyleSheet().seaborn_figure(return_figure=True)
        plt.axis("off")
        plt.table(cellText=df.values, colLabels=df.columns)
        print(df)

        # start of forest plot
        # fig, axis = StyleSheet().seaborn_figure(return_figure=True)
        sns.despine(fig, left=True, bottom=False, right=True, top=True)
        sns.set_style("white")
        axis.set(yticks=[])

        # todo This needs to be Reverse (currently the first study is plotted at the bottom but needs to be plotted at
        #  top

        # todo this needs to loop through the colours in palette in the same loop as index so each line get's its own
        #  colour
        plt.axis([min(self._data["lower_bound"]), max(self._data["upper_bound"]), 0, len(self._data.index)])
        for index, (lower, upper, effect, weight) in enumerate(zip(self._data["lower_bound"], self._data["upper_bound"],
                                                                   self._data["effect"], self._data["Relative Weight"])):
            plt.plot([lower, upper], [index+0.5, index+0.5])  # draw line
            plt.plot([effect], [index+0.5], marker="s", markersize=weight*weight_area)  # draw weighted effect

        # dotted line
        plt.plot([1, 1], [0, len(self._data.index)], "--", color="Black")
        plt.show()

        # todo These need to be put together in a Data -> Plot format

    def image_stack_figure(self, dimensions=None, z_list=None, elevation=30, rotation=45, down_sampling=6,
                           vertical_stack=True):
        """
        This stacks images in a 3D space vertically or horizontally

        :key dimensions: The square dimension you want the image to be, if not set, the largest of X Y dimensions will
            be selected by default
        :type dimensions: int | None

        :key z_list: A list of z dimensional coordinates for your graph, if left at default image plotted as flat
        :type z_list: list | None

        :key elevation: The elevation from the floor you want the camera to be
        :type elevation: int

        :key rotation: The rotation around the plots orgin you want the camera to be
        :type rotation: int

        :key down_sampling: This value will be used to divide dimensions to draw the plot.
        :type down_sampling: int

        :key vertical_stack: Stack images vertically, if False stack horizontally
        :type vertical_stack: bool

        :return: The current plot
        """

        # # Load the images
        raw_images = [mat_imread(img) for img in self._data]

        # If dimensions have not been set, set dimension to be the largest of X and Y
        if not dimensions:
            dimensions = max(max([img.shape[0] for img in raw_images]), max([img.shape[1] for img in raw_images]))

        # If not a custom z, set z to be a flat list based on index
        if not z_list:
            z_list = [np.full((dimensions, dimensions), index) for index, img in enumerate(raw_images)]

        # Read in the images and Scale images them to a square
        images = [cv2.resize(img, (dimensions, dimensions)) for img in raw_images]

        # Plot the images, depending on the sub image resolution scaling from r/cstride this can take a while so print
        # progress
        x, y = np.mgrid[0:dimensions, 0:dimensions]
        ax = plt.gca(projection='3d')
        for index, (img, z) in enumerate(zip(images, z_list)):
            # y and z are inverted if horizontal stacking
            if vertical_stack:
                ax.plot_surface(x, y, z, rstride=down_sampling, cstride=down_sampling, facecolors=img, shade=False)
            else:
                ax.plot_surface(x, z, y, rstride=down_sampling, cstride=down_sampling, facecolors=img, shade=False)
            print(f"plotted {index}")

        # Set camera in 3D space
        ax.view_init(elev=elevation, azim=rotation)
        plt.axis("off")
        self.write_plot(ax)
        return ax

    def box_plot(
        self,
        x_var,
        y_var,
        gradient_variable=None,
        custom_ranking=None,
        orientation=None,
    ):
        """Create a box plot in seaborn using the style sheet and chosen variable values.

        :param x_var: The variable you want on the x axis
        :type x_var: str
        :param y_var: The variable you want on the y axis
        :type y_var: str
        :param gradient_variable: A variable to apply a gradient of colour to the points
        :type gradient_variable: str
        :param custom_ranking: A list of rankings to use instead of the default set
        :type custom_ranking: list
        :param orientation: Whether plot should be vertical ("v") or horizontal ("h")
        :type orientation: str
        :return: The seaborn plot is returned, and .png image saved to the write directory
        :rtype: matplotlib.axes._subplots.AxesSubplot
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
            palette=self.palette(),
            linewidth=self.outline_width,
            hue=gradient_variable,
            orient=orientation,
            hue_order=custom_ranking,
            order=custom_ranking,
            ax=axis,
        )
        # # Write out the plot
        self.write_plot(plot)

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

        :param x_var: The variable you want on the x axis
        :type x_var: str
        :param y_var: The variable you want on the y axis
        :type y_var: str
        :param gradient_variable: A variable to apply a gradient of colour to the points
        :type gradient_variable: str
        :param size_variable: A variable that will be used to decide the line width
        :type size_variable: str
        :param custom_ranking: A list of rankings to use instead of the default set
        :type custom_ranking: list
        :return: The seaborn plot is returned, and .png image saved to the write directory
        :rtype: matplotlib.axes._subplots.AxesSubplot
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
            palette=self.palette(),
            hue_order=custom_ranking,
            sizes=(self.min_point_size, self.max_point_size),
            ax=axis,
        )

        # Write out the plot to chosen write directory as a png
        self.write_plot(plot)

        return plot

    def bar_plot(
            self,
            x_var,
            y_var,
            gradient_variable
    ):
        """Create a bar plot in seaborn using the style sheet and chosen variable values.

        :param x_var: The variable you want on the x axis
        :type x_var: str
        :param y_var: The variable you want on the y axis
        :type y_var: str
        :param gradient_variable: A variable to apply a gradient of colour to the points
        :type gradient_variable: str
        :param size_variable: A variable that will be used to decide the line width
        :type size_variable: str
        """

        # Validate the arguments provided
        self._validate_variable_args(locals(), locals().values(), ["custom_ranking"])

        # Set defaults before plotting
        figure, axis = plt.subplots(figsize=(self.figure_x, self.figure_y))
        sns.despine(figure, left=True, bottom=True)

        # Generate the plot
        # NB Some arguments are left at default that are given sensible defaults by seaborn
        plot = sns.barplot(
            x=x_var,
            y=y_var,
            data=self._data,
            hue=gradient_variable
        )

        # Write out the plot to chosen write directory as a png
        self.write_plot(plot)

        return plot

    def violin_plot(
            self,
            x_var,
            y_var,
            gradient_variable
    ):
        """Create a bar plot in seaborn using the style sheet and chosen variable values.

        :param x_var: The variable you want on the x axis
        :type x_var: str
        :param y_var: The variable you want on the y axis
        :type y_var: str
        :param gradient_variable: A variable to apply a gradient of colour to the points
        :type gradient_variable: str
        """

        # Validate the arguments provided
        self._validate_variable_args(locals(), locals().values(), ["custom_ranking"])

        # Set defaults before plotting
        figure, axis = plt.subplots(figsize=(self.figure_x, self.figure_y))
        sns.despine(figure, left=True, bottom=True)

        # Generate the plot
        # NB Some arguments are left at default that are given sensible defaults by seaborn
        plot = sns.violinplot(
            x=x_var,
            y=y_var,
            data=self._data,
            hue=gradient_variable
        )

        # Write out the plot to chosen write directory as a png
        self.write_plot(plot)

        return plot

    def kde_plot(
            self
    ):
        """Create a kde plot in seaborn using the style sheet and chosen variable values.

        :param x_var: The variable you want on the x axis
        :type x_var: str
        :param y_var: The variable you want on the y axis
        :type y_var: str
        """

        # Validate the arguments provided
        self._validate_variable_args(locals(), locals().values(), ["custom_ranking"])

        # Set defaults before plotting
        figure, axis = plt.subplots(figsize=(self.figure_x, self.figure_y))
        sns.despine(figure, left=True, bottom=True)

        # Generate the plot
        # NB Some arguments are left at default that are given sensible defaults by seaborn
        plot = sns.kdeplot(
            data=self._data
        )

        # Write out the plot to chosen write directory as a png
        self.write_plot(plot)

        return plot

    def residual_plot(
        self, x_var, y_var, ignore_na=True, colour=None, legend_label=None
    ):
        """Regress y_var on x_var, and then draw a scatterplot of the residuals.

        :param x_var: The variable you want on the x axis
        :type x_var: str
        :param y_var: The variable you want on the y axis
        :type y_var: str
        :param ignore_na: If True, ignore observations with missing data when fitting & plotting
        :type ignore_na: bool
        :param colour: Colour to use for all elements of the plot
        :type colour: matplotlib color
        :param legend_label: Label that will be used in plot legend
        :type legend_lable: str
        :return: The seaborn plot is returned, and .png image saved to the write directory
        :rtype: matplotlib.axes._subplots.AxesSubplot
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
        self.write_plot(plot)

        return plot

    def _set_style_sheet(self, new_style):
        """
        This takes an dict which is compared against the values set in the stylesheet, if a match is found then the
        stylesheet is updated with the new value
        :param new_style: style_sheet dictionary of keys and values to overide in class StyleSheet
        :type new_style: dict
        :return: Nothing, setattr all values for matching keys then end
        :rtype: None
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

            file_type = data.split(".")
            if len(file_type) == 1:
                files = [f.split(".")[-1] for f in os.listdir(data)]
                if "png" in files:
                    return [os.path.realpath(f"{data}/{file}") for file in os.listdir(data)]
                else:
                    raise TypeError("Only .png files are currently expected for directory iteration")

            else:
                file_type = file_type[-1]
                if file_type == "csv":
                    data = pd.read_csv(data)
                elif file_type == "xlsx":
                    data = pd.read_excel(data)
                elif file_type == "dta":
                    data = pd.read_stata(data)
                elif file_type == "sav":
                    data = pd.read_spss(data)
                else:
                    sys.exit("Error: File type not supported\nCurrent supported files are pandas.Dataframe, csv, xlsx,"
                             " dta and sav")
        return data

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


    def _set_figure_name(self, figure_name):
        """Given original filename, appends an integer to make it unique.

        :param figure_name: Chosen name of the figure
        :type: str
        :return: Unique figure_name
        :rtype: str
        """
        # Generate the output file name
        filename = figure_name
        filepath = os.path.join(self._write_directory, figure_name + ".png")

        # Check if this file if it already exists
        if os.path.isfile(filepath):
            expand = 1
            # If it does exist then add a number to the end until an available name
            while True:
                expand += 1
                new_path = filepath.split(".png")[0] + str(expand) + ".png"
                if os.path.isfile(new_path):
                    continue
                else:
                    # Return the path with correct integer at the end
                    return filename + str(expand)
        else:
            # If no changes needed, just return original filename
            return filename

    def _set_file_path(self):
        file_path = os.path.abspath(
            os.path.join(self._write_directory, self._figure_name)
        )
        return file_path

    def write_plot(self, plot):
        """Writes out plot to .png to requested location.
            This function will create the directory requested if it does not exist already.

        :param plot: Plot to write
        :type: matplotlib.axes._subplots.AxesSubplot
        :return: None
        :rtype: None
        """

        try:
            plot.get_figure().savefig(self._file_path, bbox_inches="tight", dpi=300)
        except FileNotFoundError:
            # If the subdirectory does not exist, try to make it
            Path(self._write_directory).mkdir(parents=True, exist_ok=True)
            # Try saving the plot out again
            plot.get_figure().savefig(self._file_path, bbox_inches="tight", dpi=300)
        except OSError as ex:
            # If any other errors are raised, print them to the console
            print(ex)
