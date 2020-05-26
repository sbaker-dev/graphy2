from graphy2 import sns
from graphy2 import plt
SEABORN_STYLE = ["whitegrid", "dark", "white", "ticks", "darkgrid"]


class StyleSheet:
    def __init__(self, figure_x=5, figure_y=5, number_of_colours=8, colour_palette="Blues_d",
                 outline_width=0, point_min_size=1, dpi=300, d_spline_top=True, d_spline_bottom=True,
                 d_spline_left=True, d_spline_right=True, seaborn_style="darkgrid", custom_seaborn=None):
        """
        This is the master controller for the styling of graphs and Tables within graphy2.

        :key figure_x: X length of the figure
        :type figure_x: int | float

        :key figure_y: X length of the figure
        :type figure_y: int | float

        :key number_of_colours: Number of colours to use
        :type number_of_colours: int
        
        :param colour_palette:
        :param outline_width:
        :param point_min_size:
        :param dpi:
        :param d_spline_top:
        :param d_spline_bottom:
        :param d_spline_left:
        :param d_spline_right:
        :param seaborn_style:
        """

        self.colour_palette = colour_palette
        self.number_of_colours = number_of_colours
        self.figure_x = figure_x
        self.figure_y = figure_y
        self.outline_width = outline_width
        self.min_point_size = point_min_size
        self.max_point_size = self.number_of_colours
        self.dpi = 300
        self.d_spline_top = d_spline_top
        self.d_spline_bottom = d_spline_bottom
        self.d_spline_left = d_spline_left
        self.d_spline_right = d_spline_right
        self.seaborn_style = seaborn_style
        self.custom_seaborn = custom_seaborn

        self.style_sheet = [locals(), locals().values()]

    def set_seaborn_style(self):
        """
        Set a seaborn style if it exists

        Further Information
        -----------------------
        Seaborn has a few default styles that are found in the SEABORN_STYLE global check list. However, these can be
        customised via a dictionary. If this use passes a dictionary to self.custom_seaborn, they can override the
        styles vus making their own

        :return: Nothing, set style if found and within a valid list of styles
        :rtype: None
        """
        if isinstance(self.seaborn_style, str) and self.seaborn_style in SEABORN_STYLE:
            sns.set_style(self.seaborn_style, self.custom_seaborn)

        # todo Currently this only uses seaborn styling via sns.set_style but matplotlib functionality can be exposed
        #  via sns.set

    def seaborn_figure(self):
        """
        Creates a default figures
        """
        self.set_seaborn_style()
        figure, axis = plt.subplots(figsize=(self.figure_x, self.figure_y))
        sns.despine(figure, left=self.d_spline_left, bottom=self.d_spline_bottom, right=self.d_spline_right,
                    top=self.d_spline_top)
        return axis

    def palette(self):
        """
        Returns the palette to be used
        """
        return sns.color_palette(self.colour_palette, self.number_of_colours)
