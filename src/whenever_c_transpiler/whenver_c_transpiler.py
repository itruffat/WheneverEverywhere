import os

cwd = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(os.path.dirname(cwd), "version.info"), "r") as f:
    transpiler_version = f.read()


def boolean_branch_to_c(branch, line_index):
    if branch[0] == "NEGATE":
        return f" ! ({boolean_branch_to_c(branch[1], line_index)})"
    elif branch[0] == "AND":
        return f"({boolean_branch_to_c(branch[1], line_index)}) && ({boolean_branch_to_c(branch[2], line_index)}"
    elif branch[0] == "OR":
        return f"({boolean_branch_to_c(branch[1], line_index)}) || ({boolean_branch_to_c(branch[2], line_index)})"
    elif branch[0] == "EQUALS":
        return f"({number_branch_to_c(branch[1], line_index)}) == ({number_branch_to_c(branch[2], line_index)})"
    elif branch[0] == "SMALLER_OR_EQUAL":
        return f"({number_branch_to_c(branch[1], line_index)}) <= ({number_branch_to_c(branch[2], line_index)})"
    elif branch[0] == "GREATER_OR_EQUAL":
        return f"({number_branch_to_c(branch[1], line_index)}) >= ({number_branch_to_c(branch[2], line_index)})"
    elif branch[0] == "GREATER_THAN":
        return f"({number_branch_to_c(branch[1], line_index)}) > ({number_branch_to_c(branch[2], line_index)})"
    elif branch[0] == "SMALLER_THAN":
        return f"({number_branch_to_c(branch[1], line_index)}) < ({number_branch_to_c(branch[2], line_index)})"
    else:
        raise Exception("Unknown Error")

def number_branch_to_c(array,line_index):
    if array[0] == "PURE_NUMBER":
        return f"{array[1]}"
    elif array[0] == "PLUS":
        return f"({number_branch_to_c(array[1], line_index)}) + ({number_branch_to_c(array[2], line_index)})"
    elif array[0] == "MINUS":
        return f"({number_branch_to_c(array[1], line_index)}) - ({number_branch_to_c(array[2], line_index)})"
    elif array[0] == "TIMES":
        return f"({number_branch_to_c(array[1], line_index)}) * ({number_branch_to_c(array[2], line_index)})"
    elif array[0] == "DIVIDE":
        return f"({number_branch_to_c(array[1], line_index)}) / ({number_branch_to_c(array[2], line_index)})"
    elif array[0] == "READ":
        return "get_input()"
    elif array[0] == "COUNT":
        if array[1][0] == "PURE_NUMBER":
            content = line_index.index(int(array[1][1]))
        else:
            content = f"get_line_pos({number_branch_to_c(array[1], line_index)})"
        return f"executionStack[{content}].count"
    else:
        raise Exception("Unknown Error")

def statement_branch_to_c(statement, line_index):
    if statement[0] == "PRINT":
        answer = []
        for string in statement[1]:
            answer.append(f"printf({', '.join(string_branch_to_c(string, line_index))});")
        answer += ["printf(\"\\n\");"]
        return answer
    elif statement[0] == "LINE_ADD_REMOVE":
        if statement[1][0] == "PURE_NUMBER":
            position = line_index.index(int(statement[1][1]))
            return [f"change_pos_quantity({position},{number_branch_to_c(statement[2], line_index)});"]
        else:
            return [f"change_lines_quantity({number_branch_to_c(statement[1], line_index)},{number_branch_to_c(statement[2], line_index)});"]

def string_branch_to_c(string, line_index):
    if string[0] == "PURE_STRING":
        return [f"\"%s\"", '\"'.join(["",string[1].replace('\"', '\\\"'),""])]
    elif string[0] == "UNICODE_2_CHAR":
        return [f"\"%c\"", number_branch_to_c(string[1], line_index)]
    elif string[0] == "NUMBER_2_STRING":
        return [f"\"%llu\"", number_branch_to_c(string[1], line_index)]
    else:
        raise Exception("Unknown Error")

def line_to_c_function(line, line_index):
    tab = "    "
    number, defer, again, statements = line
    position = line_index.index(number)
    answer = []
    answer.append(f"void F{position}_for_line{number}(void) {{ ")
    answer_defer = [f"{tab}bool defer = False "]
    for d in defer:
        answer_defer+= [" || " , "( " , boolean_branch_to_c(d, line_index), ")"]
    answer.append("".join(answer_defer) + ";")
    answer.append(f"{tab}if(!defer){{")
    answer_again = [f"{tab}{tab}bool again = False"]
    for a in again:
        answer_again+= [" || " , "( " , boolean_branch_to_c(a, line_index), ")"]
    answer.append("".join(answer_again) + ";")
    answer_statements = [f"{tab}{tab}// Starting statements \n"]
    for s in statements:
        for sub_s in statement_branch_to_c(s, line_index):
            answer_statements += [f"{tab}{tab}", sub_s, "\n"]
    answer_statements .append(f"{tab}{tab}// Statements done")
    answer.append("".join(answer_statements))
    answer.append(f"{tab}{tab}if(!again) change_pos_quantity({position}, -1);")
    answer.append(f"{tab}}}")
    answer.append(f"}}")

    return "\n".join(answer)

def line_to_c_initialization(line, line_index):
    tab = "    "
    number = line[0]
    position = line_index.index(number)
    answers = []
    answers += [f"{tab}lines[{position}]= (Line) {{{number}, &F{position}_for_line{number}}};"]
    answers += [f"{tab}executionStack[{position}] = (StackCount) {{{number},1}};"]
    return answers


def generate_c_code(lines, filename):

    indexes = [x[0] for x in lines]
    functions = "\n".join([line_to_c_function(line, indexes) for line in lines])
    initializations= "\n".join(["\n".join(line_to_c_initialization(line,indexes)) for line in lines])

    with open(os.path.join(cwd, "template.c"), "r") as f:
        template = f.read()

    # Will improve later
    new_code = template.replace("// <version>", f"{transpiler_version}")
    new_code = new_code.replace("// <filename>", f"{filename}")
    new_code = new_code.replace("// #define USING_WEIGHTED_RANDOM", f"#define USING_WEIGHTED_RANDOM False")
    new_code = new_code.replace("// #define TOTAL_LINES", f"#define TOTAL_LINES {len(lines)}")
    new_code = new_code.replace("//<<<LINES>>>", functions)
    new_code = new_code.replace("//<<<LINES_DEF>>", initializations)

    return new_code

if __name__ == "__main__":
        from whenever_examples.example_whenever_code import example_code2
        from whenever_parser.whenever_parser import code_to_tree

        tree = code_to_tree(example_code2, "test2", picklefy=False)
        print(generate_c_code(tree, "test2"))