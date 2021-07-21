from graphy2 import pd, sns, sys
from graphy2.StyleSheet import StyleSheet
from pathlib import Path
from graphy2.data import Data
import os
import cv2
from matplotlib.image import imread as mat_imread
import numpy as np
from csvObject import CsvObject
import matplotlib.pyplot as plt
import warnings

# required even if not used for 3D functionality in matplotlib
from mpl_toolkits.mplot3d import Axes3D

class Graphy(StyleSheet):
    def __init__(
        self, data, figure_name="Graphy_Output", style_sheet=None, write_directory=""
    ):
        super().__init__()

        if style_sheet:
            self._set_style_sheet(style_sheet)

        self._read_directory = data
        self._data = self._set_data_frame(data)
        self._write_directory = self._set_write_directory(write_directory)
        self._figure_name = self._set_figure_name(figure_name)
        self._file_path = self._set_file_path()
        self._store_data = self._set_data_frame(data)

    def forest_plot(self, weight_area=50):
        """
        Constructs a forest plot

        Notes
        ------
        Currently the formating is very data dependent and it needs to handle the output explicitly.
        Also needs to all you to actually submit what types of formation you want to do like ODDS or RR

        :param weight_area:
        :return:
        """

        # Construct the table's data
        # data, plot_data = Data(self._data).construct_odds_table()

        # Get height to set each row based on number of data entries
        # no_of_rows = data.shape[0] + 1
        # no_of_cols = data.shape[1]
        # print(self._store_data)

        # Write the forest subplot
        self._forest_plot_plot(60)

        # # Construct the table subplot
        # self._forest_plot_table(no_of_rows, data)
        #
        # # Todo this should be probably have a specific handle rather than being part of attribute error
        # self.write_plot(plt)

    def _forest_plot_plot(self, weight_area):
        # Instatiate the figure (we will recreate the axes, so don't need them)
        fig, ax2 = StyleSheet(dpi=300).seaborn_figure(return_figure=True)

        # TODO: +5 and -5 work with this number of rows/cols but this should be tested
        # with other data sets to see if it needs to be proportionate to number of rows/cols
        # Set the figure size so it's proportionate to the amount of data in the figure
        # todo Agreed, this needs to be generalised but cannot think of how to do that right now.
        fig.set_size_inches(5, 5)

        # Make sure the two subplots use available space using tight_layout()
        plt.tight_layout()
        # # Remove distance between the table and the graph
        # plt.subplots_adjust(wspace=0.1, hspace=0)

        # # Create the subplots to our data requirements (makes sure that the rows of the
        # # table will line up with the graph we draw).
        # ax2 = plt.subplot2grid(
        #     (no_of_rows, 2), (1, 1), rowspan=no_of_rows - 1, colspan=1
        # )

        # Plotting the forest plot
        # print(self._store_data)
        # print(self._store_data.iloc[:,3])
        ax2.set(xlim=(min(self._store_data.iloc[:,3]), max(self._store_data.iloc[:, 4])), ylim=(0, 10))
        # Make sure the plots are ordered correctly against the table
        plt.gca().invert_yaxis()

        # Altering the appearance of the axis ticks and labels
        ax2.tick_params(
            axis="y",  # changes apply to the x-axis
            which="both",  # both major and minor ticks are affected
            labelleft=False,  # ticks along the bottom edge are off
            top=False,
        )  # ticks along the top edge are off
        sns.despine(left=True)

        # Ensure that there are as many colours as there are values
        self.number_of_colours = 10

        # Drawing the actual lines and squares on the plot
        # print(self._store_data.values)
        # print(self.palette())
        for index, ((exposure, eff_size, se, lower, upper), colour) in enumerate(zip(self._store_data.values, self.palette())):
            # print(eff_size)
            ax2.plot([lower, upper], [index + 0.5, index + 0.5], color=colour)
            ax2.plot([eff_size], [index + 0.5], marker="s", markersize=0.1 * weight_area, color=colour)

        # Draw the dotted line
        ax2.plot([0, 0], [0, 10], "--", color="White")

        self.write_plot(plt)


    def _forest_plot_table(self, no_of_rows, data):
        """
        Construct the table subplot for forest plot

        :param no_of_rows: The number of rows in the table
        :param data: the values to put in the table
        :return: Nothing, set the table subplot then finish
        """

        # Create table axis for forest plot
        ax1 = plt.subplot2grid((no_of_rows, 2), (0, 0), rowspan=no_of_rows, colspan=1)
        ax1.axis("off")

        # Set up the table
        tbl = ax1.table(
            cellText=data.values,
            colLabels=[f"$\\bf{header}$" for header in data.columns],
            edges="open",
            loc="center",
            cellLoc="center",
        )

        # Underlines column headers
        self._table_under_line_row(tbl, "B", 0)

        # These lines set the row height so that they fit the plot.
        # This ensures each row is sized to line up with the plot on the right.
        for cell in tbl.properties()["children"]:
            cell.set_height(1 / no_of_rows)

        # Now, align the columns as desired.
        self._table_align_columns(tbl, col=0, align="left")

        # Autoset column width (Beware if the no of cols changes, this may mean the plot
        # exceeds it's subplot space...) # todo why?
        tbl.auto_set_column_width([i for i in range(len(data.columns))])

        # todo font size should be an exposed stylesheet parameter
        # Both lines required for font size to be changed (who knows why...)
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(10)

    @staticmethod
    def _table_under_line_row(table, underline_side, row_index):
        """
        Underlines row

        :param table: table in question
        :param underline_side: Takes B, R, T, or L for bottom right top or left or open, closed horizontal vertical
        :param row_index: Row to under line
        :return: None
        """
        cells = [key for key in table._cells if key[0] == row_index]
        for cell in cells:
            table._cells[cell].visible_edges = underline_side

    @staticmethod
    def _table_align_columns(table, col, align="left"):
        """
        Aligns table

        Source: https://stackoverflow.com/questions/48210749/matplotlib-table-assign-different-text-alignments-to-
                different-columns

        :param table: table in question
        :param col: column index
        :param align: align type
        :return: None
        """
        cells = [key for key in table._cells if key[1] == col]
        for cell in cells:
            table._cells[cell]._loc = align

    def image_stack_figure(
        self,
        dimensions=None,
        z_list=None,
        elevation=30,
        rotation=45,
        down_saing=6,
        vertical_stack=True,
    ):
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
            dimensions = max(
                max([img.shape[0] for img in raw_images]),
                max([img.shape[1] for img in raw_images]),
            )

        # If not a custom z, set z to be a flat list based on index
        if not z_list:
            z_list = [
                np.full((dimensions, dimensions), index)
                for index, img in enumerate(raw_images)
            ]

        # Read in the images and Scale images them to a square
        images = [cv2.resize(img, (dimensions, dimensions)) for img in raw_images]

        # Plot the images, depending on the sub image resolution scaling from r/cstride this can take a while so print
        # progress
        x, y = np.mgrid[0:dimensions, 0:dimensions]
        ax = plt.gca(projection="3d")
        for index, (img, z) in enumerate(zip(images, z_list)):
            # y and z are inverted if horizontal stacking
            if vertical_stack:
                ax.plot_surface(
                    x,
                    y,
                    z,
                    rstride=down_saing,
                    cstride=down_saing,
                    facecolors=img,
                    shade=False,
                )
            else:
                ax.plot_surface(
                    x,
                    z,
                    y,
                    rstride=down_saing,
                    cstride=down_saing,
                    facecolors=img,
                    shade=False,
                )
            print(f"plotted {index}")

        # Set camera in 3D space
        ax.view_init(elev=elevation, azim=rotation)
        plt.axis("off")
        self.write_plot(ax)
        return ax

    def pie_chart(self, start_angle=90, display_values=None):

        warnings.warn("Deprecated: Will be moved into Seaborn.py soon.tm", DeprecationWarning)

        # Easier to use a csv object rather than pandas for this so recast the data to CsvObject
        labels, amount, explode = CsvObject(
            self._read_directory, column_types=[str, int, float]
        ).column_data

        # Construct the pie chart from the raw data
        ax = self.seaborn_figure()
        ax.pie(
            amount,
            explode=explode,
            labels=labels,
            startangle=start_angle,
            colors=self.palette(),
            autopct=display_values,
        )
        ax.axis("equal")
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
        warnings.warn("Deprecated: Will be moved into Seaborn.py soon.tm", DeprecationWarning)


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
        warnings.warn("Deprecated: Will be moved into Seaborn.py soon.tm", DeprecationWarning)

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

    def bar_plot(self, x_var, y_var, gradient_variable):
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
        warnings.warn("Deprecated: Will be moved into Seaborn.py soon.tm", DeprecationWarning)

        # Validate the arguments provided
        self._validate_variable_args(locals(), locals().values(), ["custom_ranking"])

        # Set defaults before plotting
        figure, axis = plt.subplots(figsize=(self.figure_x, self.figure_y))
        sns.despine(figure, left=True, bottom=True)

        # Generate the plot
        # NB Some arguments are left at default that are given sensible defaults by seaborn
        plot = sns.barplot(x=x_var, y=y_var, data=self._data, hue=gradient_variable)

        # Write out the plot to chosen write directory as a png
        self.write_plot(plot)

        return plot

    def violin_plot(self, x_var, y_var, gradient_variable):
        """Create a bar plot in seaborn using the style sheet and chosen variable values.

        :param x_var: The variable you want on the x axis
        :type x_var: str
        :param y_var: The variable you want on the y axis
        :type y_var: str
        :param gradient_variable: A variable to apply a gradient of colour to the points
        :type gradient_variable: str
        """
        warnings.warn("Deprecated: Will be moved into Seaborn.py soon.tm", DeprecationWarning)

        # Validate the arguments provided
        self._validate_variable_args(locals(), locals().values(), ["custom_ranking"])

        # Set defaults before plotting
        figure, axis = plt.subplots(figsize=(self.figure_x, self.figure_y))
        sns.despine(figure, left=True, bottom=True)

        # Generate the plot
        # NB Some arguments are left at default that are given sensible defaults by seaborn
        plot = sns.violinplot(x=x_var, y=y_var, data=self._data, hue=gradient_variable)

        # Write out the plot to chosen write directory as a png
        self.write_plot(plot)

        return plot

    def kde_plot(self):
        """Create a kde plot in seaborn using the style sheet and chosen variable values.

        :param x_var: The variable you want on the x axis
        :type x_var: str
        :param y_var: The variable you want on the y axis
        :type y_var: str
        """
        warnings.warn("Deprecated: Will be moved into Seaborn.py soon.tm", DeprecationWarning)

        # Validate the arguments provided
        self._validate_variable_args(locals(), locals().values(), ["custom_ranking"])

        # Set defaults before plotting
        figure, axis = plt.subplots(figsize=(self.figure_x, self.figure_y))
        sns.despine(figure, left=True, bottom=True)

        # Generate the plot
        # NB Some arguments are left at default that are given sensible defaults by seaborn
        plot = sns.kdeplot(data=self._data)

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

        warnings.warn("Deprecated: Will be moved into Seaborn.py soon.tm", DeprecationWarning)

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
                    sys.exit(
                        "Error: File type not supported\nCurrent supported files are pandas.Dataframe, csv, xlsx,"
                        " dta and sav"
                    )
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

        plot.rcParams.update({
            "figure.facecolor": (0.0, 0.0, 0.0, 1.0),
            "axes.facecolor": (1.0, 1.0, 1.0, 0.0),
            "savefig.transparent": True,
        })

        try:
            # print("HERE?")
            # print(plot.rcParams)
            plot.get_figure().savefig(self._file_path, bbox_inches="tight", dpi=300)

        except FileNotFoundError:
            # If the subdirectory does not exist, try to make it
            Path(self._write_directory).mkdir(parents=True, exist_ok=True)
            # Try saving the plot out again
            plot.get_figure().savefig(self._file_path, bbox_inches="tight", dpi=300)

        except AttributeError:
            plot.savefig(self._file_path, dpi=300, bbox="tight")

        except OSError as ex:
            # If any other errors are raised, print them to the console
            print(ex)
