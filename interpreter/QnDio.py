# Quick and Dirty IO Handler, replace with something better in the future

output_to_file = False
output_file = ""

input_from_file = False
input_file = ""
input_file_kill_after_done = False
_input_file_left = []
_input_kill=False

def get_input():
    global input_file
    global input_from_file
    global input_file_kill_after_done
    global _input_file_left
    global _input_kill

    if _input_kill:
        report_error("Input ended", 2)

    if not input_from_file:
        answer = input()
    else:
        if len(_input_file_left) == 0 and input_file != "":
            with open(input_file,"r") as f:
                _input_file_left = f.readlines()
            input_file = ""
        answer = _input_file_left.pop(0)
        if len(_input_file_left) == 0:
            input_from_file = False
            if input_file_kill_after_done:
                _input_kill = True
    return answer

def give_output(output):
    if not output_to_file:
        print(output)
    else:
        with open(output_file, "a") as f:
            f.write(str(output)+"\n")

def report_error(error, code):
    if code == 0:
        print(error)
    else:
        raise Exception(error)