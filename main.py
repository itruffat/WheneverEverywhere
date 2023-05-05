import os, sys

if os.getenv("PYTHON_HOT_LOAD_VENV", default=0) == 1: # This line allows the use without having to activate the venv
    exec(open("venv/Scripts/activate_this.py").read(), {'__file__': "venv/Scripts/activate_this.py"})

from wparser.whenever_parser import code_to_tree
from interpreter.whenever_interpreter import interprete_tree
from c_transpiler.whenver_c_transpiler import generate_c_code
import interpreter.QnDio as io

io.output_to_file = False
io.output_file = "output.txt"

if __name__ == '__main__':

    if len(sys.argv) < 3:
        io.report_error("Invalid amount of parameters, need a mode (c/run) and the name of the code snippet to run", 2)

    mode = sys.argv[1]

    if mode not in ["run", "c"]:
        io.report_error("Invalid mode, use run/c", 2)

    if len(sys.argv) > 3:
        save = True
        output_name = sys.argv[3]
    else:
        save = False
        output_name = "output.c"

    file_path = sys.argv[2]

    if not os.path.exists(file_path):
        io.report_error("Can not find the file", 3)

    with open(file_path, 'r') as file:
        file_contents = file.read()

    tree = code_to_tree(file_contents, file_path, picklefy=False)

    if mode == "run":
        interprete_tree(tree)
    elif mode == "c":
        code = generate_c_code(tree, os.path.basename(file_path))

        print(code)

        if not save:
            save = input("Do you want to save to file? (y/N)")

        if save:
            with open(output_name, 'w') as file:
                file.write(code)
    else:
        io.report_error("unknown mode", 2)