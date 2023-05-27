from random import choice
from WheneverEverywhere.whenever_interpreter.QnDio import give_output, get_input, report_error

inputs = []

def input_getter_f():
    global inputs
    while True:
        _inputs = get_input()
        for i in _inputs:
            if i.isnumeric():
                if len(inputs) > 0 and type(inputs[-1]) is str:
                    inputs[-1] += i
                else:
                    inputs.append(i)
            else:
                inputs.append(ord(i))
        while inputs:
            yield int(inputs.pop(0))

input_getter = input_getter_f()

class Line():
    def __init__(self, number, defer, again, statements):
        self.number = number
        self.defer = defer
        self.again = again
        self.statements = statements

def resolve_numbers(array):
    if array[0] == "PURE_NUMBER":
        return array[1]
    elif array[0] == "PLUS":
        return resolve_numbers(array[1]) + resolve_numbers(array[2])
    elif array[0] == "MINUS":
        return resolve_numbers(array[1]) - resolve_numbers(array[2])
    elif array[0] == "TIMES":
        return resolve_numbers(array[1]) * resolve_numbers(array[2])
    elif array[0] == "DIVIDE":
        return resolve_numbers(array[1]) // resolve_numbers(array[2])
    elif array[0] == "READ":
        return int(next(input_getter))
    elif array[0] == "COUNT":
        count_line = resolve_numbers(array[1])
        if active_lines is None or count_line not in active_lines.keys():
            return 0
        else:
            return active_lines[count_line]
    else:
        print(array[0])
        report_error("Unknown Error", 2)

def resolve_boolean(array):
    if array[0] == "NEGATE":
        return not(resolve_boolean(array[1]))
    elif array[0] == "AND":
        return resolve_boolean(array[1]) and resolve_boolean(array[2])
    elif array[0] == "OR":
        return resolve_boolean(array[1]) or resolve_boolean(array[2])
    elif array[0] == "EQUALS":
        return resolve_numbers(array[1]) == resolve_numbers(array[2])
    elif array[0] == "SMALLER_OR_EQUAL":
        return resolve_numbers(array[1]) <= resolve_numbers(array[2])
    elif array[0] == "GREATER_OR_EQUAL":
        return resolve_numbers(array[1]) >= resolve_numbers(array[2])
    elif array[0] == "GREATER_THAN":
        return resolve_numbers(array[1]) >  resolve_numbers(array[2])
    elif array[0] == "SMALLER_THAN":
        return resolve_numbers(array[1]) <  resolve_numbers(array[2])
    else:
        report_error("Unknown Error")

def resolve_strings(array):
    new_arrray = []
    for string in array:
        if string[0] == "PURE_STRING":
            new_arrray.append(string[1])
        elif string[0] == "UNICODE_2_CHAR":
            number = resolve_numbers(string[1])
            new_arrray.append(chr(number))
        elif string[0] == "NUMBER_2_STRING":
            number = resolve_numbers(string[1])
            new_arrray.append(str(number))
        else:
            report_error("Unknown Error")
    return "".join(new_arrray)

def resolve_statement(statement):
    if statement[0] == "PRINT":
        give_output(resolve_strings(statement[1]))
    elif statement[0] == "LINE_ADD_REMOVE":
        line_number = resolve_numbers(statement[1])
        repetitions = resolve_numbers(statement[2])
        if line_number < 0:
            line_number = -1 * line_number
            repetitions = -1 * repetitions
        if line_number in lines.keys():
            if line_number not in active_lines.keys():
                active_lines[line_number] = 0
            active_lines[line_number] += repetitions
            if active_lines[line_number] <= 0:
                del active_lines[line_number]



def resolve_line(line_number):

    answer_defer = False
    for defer in lines[line_number].defer:
        answer_defer = answer_defer or resolve_boolean(defer)
    if not answer_defer:

        answer_again = (len(lines[line_number].again) > 0)
        for again in lines[line_number].again:
            answer_again = answer_again and resolve_boolean(again)

        for statement in lines[line_number].statements:
            resolve_statement(statement)

        if not answer_again:
            resolve_statement(('LINE_ADD_REMOVE', ('PURE_NUMBER', line_number), ('PURE_NUMBER', -1)))

def interprete_tree(tree):
    global lines
    global active_lines

    lines = {}
    active_lines = {}
    for branch in tree:
        line = Line(*branch)
        lines[line.number] = line
        active_lines[line.number] = 1

    while len(active_lines.keys()) > 0 :
        k = list(active_lines.keys())
        n = choice(k)
        resolve_line(n)


if __name__ == "__main__":
        from whenever_examples.example_whenever_code import example_code2
        from whenever_parser.whenever_parser import code_to_tree, load_tree
        code_to_tree(example_code2, "test2")
        tree = load_tree("test2")
        interprete_tree(tree)
