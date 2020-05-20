from graphy2 import sys
from graphy2.core import Graphy

if __name__ == '__main__':
    # Rgraphy2 Null args don't get passed as system arguments, but False will be passed as a string rather than as a
    # bool so args needs formatting so that a False String returns a None type
    args = []
    for arg in sys.argv:
        if "FALSE" in arg:
            args.append(None)
        else:
            args.append(arg)

    try:
        function_name = args[1]
    except IndexError as e:
        raise Exception("No arguments passed to graphy_call.py") from e

    try:
        class_args = [args[i] for i in range(2, 6)]
    except IndexError as e:
        raise Exception("Not enough arguments passed to graphy_call.py for the class args. Args should be:\n"
                        "[0]Script_name\n[1]class_method_name\n[2]path_to_data_file\n[3]write_directory\n"
                        "[4]figure_name\n[5]style_sheet\n[6+]args for class_method_name")

    method_args = [args[i] for i in range(6, len(args))]

    getattr(Graphy(*class_args), str(function_name))(*method_args)
