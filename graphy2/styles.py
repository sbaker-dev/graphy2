from graphy2 import sns


class StyleSheet:
    def __init__(self, figure_x=5, figure_y=5, number_of_colours=8, colour_palette="Blues_d",
                 outline_width=0, point_min_size=1):
        self.figure_x = figure_x
        self.figure_y = figure_y
        self.palette = sns.color_palette(n_colors=number_of_colours, palette=colour_palette)
        self.outline_width = outline_width
        self.min_point_size = point_min_size
        self.max_point_size = number_of_colours
        self.style_sheet = [locals(), locals().values()]
