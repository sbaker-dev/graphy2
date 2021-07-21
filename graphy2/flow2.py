from imageObjects.ImageMaker import ImageMaker
import cv2

from graphy2.Flow import Flow
from graphy2 import default_style_sheet



# class Flow:
#     def __init__(self):
#         self.prisma = {}
#
#     def add_to_flow(self, text, x_position, y_position):
#         self.prisma[len(self.prisma.keys())] = {"x": x_position, "y": y_position, "text": text}
#
#     def create_text_box(self, text):
#         current_box = ImageMaker().create_text_box(text, cv2.FONT_HERSHEY_SIMPLEX, 35)
#         current_box.inset_rounded_border((255, 0, 0), 5, 25, 0.1)
#
#         current_box.show()
#         return current_box
#
#
#     def _construct_flow_columns(self):
#
#         # Create columns of x's
#         columns = sorted(list(set([values["x"] for values in self.prisma.values()])))
#
#         column_images = {}
#         for col in columns:
#             # Sort on Y position within a given x
#             column_values = {value["y"]: value["text"] for value in self.prisma.values() if value["x"] == col}
#
#             # Create a text box for each row in a given column
#             column_images[col] = {key: self.create_text_box(text)
#                                   for key, text in zip(column_values.keys(), column_values.values())}
#         return column_images
#
#     @staticmethod
#     def flow_bound(bound, columns, spacing=None):
#         """
#         We need to set the image bounds to be equal to the largest or widest column
#
#         :param bound: The bound, height or width
#         :param spacing: The amount of spacing of y or x
#         :param columns: The dict of columns
#         :return: The max bound of x or y given spacing
#         """
#
#         if spacing:
#             return max([sum([getattr(image, bound) for image in v]) + (spacing * (len(v) - 1))
#                         for v in columns.values()])
#         else:
#             return max([max([getattr(image, bound) for image in v])
#                         for v in columns.values()])
#
#     def _get_bounds(self, columns, key):
#         return [getattr(row, key) for col in columns.values() for row in col.values()]
#
#     def construct_flow(self, canvas_colour, x_spacing=1.5):
#
#         columns = self._construct_flow_columns()
#         widths = {key: max(self._get_bounds(columns, "width")) for key in columns.keys()}
#         height = max([sum(self._get_bounds(columns, "height")) for _ in columns.keys()])
#
#         # Define the canvas
#         canvas = ImageMaker().create_blank(int(sum(v for v in widths.values()) * x_spacing), height)
#         canvas.colour_covert()
#         canvas.change_a_colour((0, 0, 0), canvas_colour)
#
#         for index, image_list in zip(columns.keys(), columns.values()):
#             for i, (y_placer, image) in enumerate(zip(image_list.keys(), image_list.values())):
#                 canvas.overlay_image(image, int(y_placer * image.height), 0 + int((index * widths[index]) * x_spacing))
#
#         canvas.show()
#

# flow_obj = Flow()
#
# flow_obj.add_to_flow("UK Biobank Population: 502,507", 0, 0)
# flow_obj.add_to_flow("Born in scotland: 50,000", 1, 1)
# flow_obj.add_to_flow("Uk Biobank Population not in scotland: 450,000", 0, 1)
# flow_obj.construct_flow((255, 255, 255))



# custom_style = default_style_sheet()
# custom_style["figure_x"] = 8
# custom_style["figure_y"] = 12
#
#
# obj = Flow(r"I:\Work\Figures_and_tables\Scarlet_Long_Term\Figures", "Flow Plot Re", 20, custom_style
#            )
#
# # Add a bunch of sample information
# obj.add_to_flow("UK Biobank Population", 502507)
# obj.add_to_flow("Born in Scotland", 502507, add=False)
# obj.add_to_flow("UK Biobank Population not in scotland", 502507)
# obj.add_to_flow("No Birth Coordinate", 502507, add=False)
# obj.add_to_flow("UK Biobank Population that can be geolocated", 502507)
# obj.add_to_flow("Born Before 1941", 502507, add=False)
# obj.add_to_flow("UK Biobank Population within year sample range", 502507)
# obj.add_to_flow("Missing Data", 502507, add=False)
# obj.add_to_flow("UK Biobank sample Population", 502507)
#
# # Write out the plot
# obj.construct_flow_plot(column_mod=1.05)