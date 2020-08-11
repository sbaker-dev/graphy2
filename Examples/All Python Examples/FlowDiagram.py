from graphy2.StyleSheet import default_style_sheet
from graphy2.Custom_Graphs.Flow import Flow

if __name__ == '__main__':
    # Change default style so that the diagram will fit, do some trail an error
    custom_style = default_style_sheet()
    custom_style["figure_x"] = 8
    custom_style["figure_y"] = 12

    # Create flow object, with custom style
    obj = Flow(r"C:\Users\Samuel\PycharmProjects\graphy2\Examples\All Python Examples\plots", "Flow Plot", 20,
               custom_style)

    # Add a bunch of sample information
    obj.add_to_flow("UK Biobank Population", 502507)
    obj.add_to_flow("Born in Scotland", 502507, add=False)
    obj.add_to_flow("UK Biobank Population not in scotland", 502507)
    obj.add_to_flow("No Birth Coordinate", 502507, add=False)
    obj.add_to_flow("UK Biobank Population that can be geolocated", 502507)
    obj.add_to_flow("Born Before 1941", 502507, add=False)
    obj.add_to_flow("UK Biobank Population within year sample range", 502507)
    obj.add_to_flow("Missing Data", 502507, add=False)
    obj.add_to_flow("UK Biobank sample Population", 502507)

    # Write out the plot
    obj.construct_flow_plot(column_mod=1.03)
