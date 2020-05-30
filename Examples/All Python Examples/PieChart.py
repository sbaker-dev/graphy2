from graphy2.core import Graphy

if __name__ == '__main__':

    # Load in a csv with Labels, Amount, Explode columns
    read_data = r"C:\Users\Samuel\PycharmProjects\graphy2\ExampleData\Pie.csv"

    # Create the pie chart
    Graphy(read_data, "Pie Plot").pie_chart()
