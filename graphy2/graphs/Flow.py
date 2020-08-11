from graphy2.StyleSheet import StyleSheet
from graphy2 import plt
from graphy2.Common import Common
import textwrap

class Flow(Common, StyleSheet):
    def __init__(self, write_directory, figure_name, line_max):
        super().__init__(write_directory=write_directory, file_name=figure_name)
        self._prisma_dict = {}
        self.line_max = line_max

    def add_to_flow(self, title, number, add=True):
        self._prisma_dict[len(self._prisma_dict.keys()) + 1] = {"Add": add, "Title": title, "N": number}

    def _set_y(self, y, key, key_modifier=0):
        return (y / len(self._prisma_dict.keys())) * (key + key_modifier)



    def _format_text(self, value):
        return f"{textwrap.fill(value['Title'], self.line_max)}\n\nN={value['N']}"


    def construct_prisma_plot(self, padding=0.1, column_mod=1.0):
        print(self._prisma_dict)
        self.figure_x = 8
        self.figure_y = 12

        fig, axis = self.seaborn_figure(return_figure=True)
        x = int(self.figure_x * 100)
        y = int(self.figure_y * 100)
        r = fig.canvas.get_renderer()
        plt.axis([0, x, 0, y])
        plt.axis("off")

        for key, value in zip(self._prisma_dict.keys(), list(self._prisma_dict.values())[::-1]):
            print(value)
            print(key)

            if value["Add"]:
                # Plot the left hand column text
                t = plt.text(int(x / 3), self._set_y(y, key), self._format_text(value),
                             ha="center", va="top", fontsize=20, wrap=True,
                             bbox=dict(boxstyle="round", facecolor="white", ec="black"))

                height = t.get_window_extent(renderer=r).height

                # Draw a line between this box and the next
                plt.plot([int(x / 3), int(x / 3)],
                         [self._set_y(y, key), self._set_y(y, key, 1) + height],
                         color="black")

            else:
                t = plt.text(int(x*(1-padding)), ((self._set_y(y, key) + self._set_y(y, key, -1)) / 2) * column_mod,
                             self._format_text(value), ha="center", va="top", fontsize=20, wrap=True,
                             bbox=dict(boxstyle="round", facecolor="white", ec="black"))

                height = t.get_window_extent(renderer=r).height



                # Horizontal line *currently an arrow
                # todo Currently getting height from the removed, but ideally we would get the last position + hieght
                plt.arrow(int(x/3), (((self._set_y(y, key) + self._set_y(y, key, -1)) / 2) - (height / 2)) * column_mod,
                          int(x * (1 - padding)), 0, head_width=5, head_length=5, fc="k", ec="k")

        plt.savefig("A")




obj = Flow(r"I:\Work\Figures and tables\Scarlet Long Term\Figures", "Prisma", 20)

obj.add_to_flow("UK Biobank Population", 502507)
obj.add_to_flow("Born in Scotland", 502507, add=False)
obj.add_to_flow("UK Biobank Population not in scotland", 502507)
obj.add_to_flow("No Birth Coordinate", 502507, add=False)
obj.add_to_flow("UK Biobank Population that can be geolocated", 502507)
obj.add_to_flow("Born Before 1941", 502507, add=False)
obj.add_to_flow("UK Biobank Population within year sample range", 502507)
obj.add_to_flow("Missing Data", 502507, add=False)
obj.add_to_flow("UK Biobank sample Population", 502507)


obj.construct_prisma_plot(column_mod=1.03)







# fig, axis = StyleSheet().seaborn_figure(return_figure=True)
#
# print()
# dimensions = fig.canvas.get_renderer()
#
# # fig = plt.figure()
# plt.axis([0, int(dimensions.width), 0, 500])
# plt.axis("off")
#
# a_mnumber = 5
# t = plt.text(250, 500, f"{5} Some Number \nthis is a bery long\n lineaed\n asdasdas dasd as d", ha="center", va="top", fontsize=20, wrap=True, bbox=dict(boxstyle="round", facecolor="white", ec="black"))
# bb = t.get_window_extent(renderer=r)
# width = bb.width
# height = bb.height
#
# a = r.width
# print(f"Width and hiehgt are {r.width}, {r.height}")
# print(a)
#
# print(width)
# print(height)
#
#
# plt.arrow(25, 90, 0, -50, head_width=5, head_length=5, fc="k", ec="k")
#
# plt.savefig("A")