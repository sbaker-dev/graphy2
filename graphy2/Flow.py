from graphy2.StyleSheet import StyleSheet
from graphy2 import plt
from graphy2.Common import Common
import textwrap


class Flow(Common, StyleSheet):
    """
    This will create a two column flow chart, similar in principle to PRISMA, but to show why you have removed
    observations from a study for example.
    """
    def __init__(self, write_directory, figure_name, line_max, style_sheet=None):
        super().__init__(write_directory=write_directory, file_name=figure_name)
        self._prisma_dict = {}
        self.line_max = line_max

        if style_sheet:
            self._set_style_sheet(style_sheet)

    def add_to_flow(self, title, number, add=True):
        """
        Add an element to the flow chart with the title of title, the value of N and then place it based on if we are
        removing it or not

        """
        self._prisma_dict[len(self._prisma_dict.keys()) + 1] = {"Add": add, "Title": title, "N": number}

    def _set_y(self, y, key, key_modifier=0):
        """
        Set the y value be equal to y divided by the number of elements times the current key to get evenly spaced
        elements
        """
        return (y / len(self._prisma_dict.keys())) * (key + key_modifier)

    def _format_text(self, value):
        """
        Format the text to be no longer than line max, with a line break between the text and the number
        """
        return f"{textwrap.fill(value['Title'], self.line_max)}\n\nN={value['N']}"

    def construct_flow_plot(self, padding=20, column_mod=1.0):
        """
        Construct a flow plot from the dict values, with padding in x and y from padding and column mod
        """
        fig, axis = self.seaborn_figure(return_figure=True)

        # Matplotlib will create an image 100 times the value we use, so we need to set x and y accordingly
        # todo set a matplotlib x and y in Stylesheet
        x = int(self.figure_x * 100)
        y = int(self.figure_y * 100)

        # Todo Return rendered from seaborn figure
        r = fig.canvas.get_renderer()
        plt.axis([0, x, 0, y])
        plt.axis("off")

        for key, value in zip(self._prisma_dict.keys(), list(self._prisma_dict.values())[::-1]):

            if value["Add"]:
                print(self._set_y(y, key))
                # Plot the left hand column text
                t = plt.text(int(x * (1 / 3)) - padding, self._set_y(y, key), self._format_text(value),
                             ha="center", va="top", fontsize=20, wrap=True,
                             bbox=dict(boxstyle="round", facecolor="white", ec="black"))

                print(t.get_window_extent)

                # Draw a line between this box and the next
                plt.plot([int(x * (1 / 3)) - padding, int(x * (1 / 3)) - padding],
                         [self._set_y(y, key), self._set_y(y, key, 1) + t.get_window_extent(renderer=r).height],
                         color="black")

            else:
                # Otherwise draw the boxes on the other side of page, modified with padding for x and column_mod for y
                t = plt.text(int(x * (2 / 3)) + padding, ((self._set_y(y, key) + self._set_y(y, key, -1)) / 2) * column_mod,
                             self._format_text(value), ha="center", va="top", fontsize=20, wrap=True,
                             bbox=dict(boxstyle="round", facecolor="white", ec="black"))

                # Horizontal line *currently an arrow*, to the center line
                height = t.get_window_extent(renderer=r).height
                plt.arrow(int(x * (1 / 3)) - padding, (((self._set_y(y, key) + self._set_y(y, key, -1)) / 2) - (height / 2)) * column_mod,
                          int(x * (2 / 3)) + padding, 0, head_width=5, head_length=5, fc="k", ec="k")


        self.write_plot(plt)
        plt.show()
