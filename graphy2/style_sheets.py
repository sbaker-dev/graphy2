from graphy2.styles import StyleSheet
from graphy2 import sns


def blank_style_sheet():
    blank = {}
    for key in StyleSheet().style_sheet[0]:
        if key != "self":
            blank[key] = ""
    return blank


def default_style_sheet():
    default = {}
    for key, value in zip(StyleSheet().style_sheet[0], StyleSheet().style_sheet[1]):
        if key != "self":
            default[key] = value
    return default


BLUE_ON_WHITE_GRID = {'figure_x': 5, 'figure_y': 5, 'number_of_colours': 8, 'colour_palette': "Blues_d",
                      'outline_width': 0, 'point_min_size': 1, 'dpi': 300, 'd_spline_top': True,
                      'd_spline_bottom': True, 'd_spline_left': True, 'd_spline_right': True,
                      'seaborn_style': 'whitegrid', 'custom_seaborn': None}

COOL_ON_WHITE = {'figure_x': 10, 'figure_y': 5, 'number_of_colours': 8,
                 'colour_palette': sns.cubehelix_palette(8, start=.5, rot=-.75), 'outline_width': 0,
                 'point_min_size': 1, 'dpi': 300, 'd_spline_top': True, 'd_spline_bottom': True, 'd_spline_left': True,
                 'd_spline_right': True, 'seaborn_style': None, 'custom_seaborn': None}
