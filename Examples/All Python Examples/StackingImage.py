from graphy2.core import Graphy


if __name__ == '__main__':

    # Set the directory where your images are stored
    data = r"Path\To\Images"

    # Set the size to bound your images too, and then the 3D position of the camera that will view your graph
    Graphy(data, "Stacking Images").image_stack_figure(down_sampling=10, elevation=15, rotation=30)
