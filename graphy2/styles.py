from graphy2 import sns, plt
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
        
        :key colour_palette: The colour palette to be used, can take a string name of a palette or a seaborn
        :type colour_palette: str | list

        :key outline_width: How wide of an outline to use
        :type outline_width: int | float

        :key point_min_size: Minimm size of a point in a graph
        :type point_min_size: int | float

        :key dpi: Resolution of the plotted figure
        :type dpi: int

        :key d_spline_top: De-spline Top
        :type d_spline_top: bool

        :key d_spline_bottom: De-spline Top
        :type d_spline_bottom: bool

        :key d_spline_left: De-spline Top
        :type d_spline_left: bool

        :key d_spline_right: De-spline Top
        :type d_spline_right: bool

        :key seaborn_style: General stylising via seaborn styles
        :type seaborn_style: str

        :key custom_seaborn: Dict of values to replace in seaborn style
        :type custom_seaborn: dict
        """

        self.figure_x = figure_x
        self.figure_y = figure_y
        self.number_of_colours = number_of_colours
        self.colour_palette = colour_palette
        self.outline_width = outline_width
        self.min_point_size = point_min_size
        self.max_point_size = self.number_of_colours
        self.dpi = dpi
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
