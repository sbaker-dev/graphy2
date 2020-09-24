from imageObjects.ImageMaker import ImageMaker
import cv2


class Flow:
    def __init__(self):
        self.prisma = {}

    def add_to_flow(self, text, x_position, y_position):
        self.prisma[len(self.prisma.keys())] = {"x": x_position, "y": y_position, "text": text}

    def _construct_flow_columns(self):

        # Create columns of x's
        columns = sorted(list(set([values["x"] for values in self.prisma.values()])))

        column_images = {}
        for col in columns:
            # Sort on Y position within a given x
            column_values = {value["y"]: value["text"] for value in self.prisma.values() if value["x"] == col}

            # Create a text box for each row in a given column
            column_images[col] = {key: ImageMaker().create_text_box(text, cv2.FONT_HERSHEY_SIMPLEX, 35)
                                  for key, text in zip(column_values.keys(), column_values.values())}
        return column_images

    @staticmethod
    def flow_bound(bound, columns, spacing=None):
        """
        We need to set the image bounds to be equal to the largest or widest column

        :param bound: The bound, height or width
        :param spacing: The amount of spacing of y or x
        :param columns: The dict of columns
        :return: The max bound of x or y given spacing
        """

        if spacing:
            return max([sum([getattr(image, bound) for image in v]) + (spacing * (len(v) - 1))
                        for v in columns.values()])
        else:
            return max([max([getattr(image, bound) for image in v])
                        for v in columns.values()])

    def _get_bounds(self, columns, key):
        return [getattr(row, key) for col in columns.values() for row in col.values()]

    def construct_flow(self, canvas_colour, x_spacing=1.5):

        columns = self._construct_flow_columns()
        widths = {key: max(self._get_bounds(columns, "width")) for key in columns.keys()}
        height = max([sum(self._get_bounds(columns, "height")) for _ in columns.keys()])

        # Define the canvas
        canvas = ImageMaker().create_blank(int(sum(v for v in widths.values()) * x_spacing), height)
        canvas.colour_covert()
        canvas.change_a_colour((0, 0, 0), canvas_colour)

        for index, image_list in zip(columns.keys(), columns.values()):
            for i, (y_placer, image) in enumerate(zip(image_list.keys(), image_list.values())):
                canvas.overlay_image(image, int(y_placer * image.height), 0 + int((index * widths[index]) * x_spacing))

        canvas.show()


flow_obj = Flow()

flow_obj.add_to_flow("UK Biobank Population: 502,507", 0, 0)
flow_obj.add_to_flow("Born in scotland: 50,000", 1, 1)
flow_obj.add_to_flow("Uk Biobank Population not in scotland: 450,000", 0, 1)
flow_obj.construct_flow((255, 255, 255))



#
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
# obj.construct_flow_plot(column_mod=1.03)