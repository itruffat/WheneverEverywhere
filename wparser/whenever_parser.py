import ply.yacc as yacc
import ply.lex as lex
import pickle

implemented_functions = ('COUNT', 'UNICODE', 'PRINT', 'READ', 'AGAIN', 'DEFER', 'FORGET')

tokens = (
             'NUMBER', 'AND', 'OR',
             'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
             'GREATER_THAN', 'SMALLER_THAN', 'GREATER_OR_EQUAL', 'SMALLER_OR_EQUAL',
             'LPAREN', 'RPAREN', 'STRING', 'THEN', 'END', 'HASH', 'NEGATE'
         ) + implemented_functions

t_STRING = r'"[^"]*"'

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'=='
t_GREATER_THAN = r'>'
t_GREATER_OR_EQUAL = r'>='
t_SMALLER_THAN = r'<'
t_SMALLER_OR_EQUAL= r'<='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_AND= r'&&'
t_OR= r'\|\|'
t_HASH= r'\#'
t_THEN = r'\,'
t_NEGATE= r'!'
t_END= r';'

t_COUNT = r'N'
t_UNICODE = r'U'
t_PRINT = r'print'
t_READ = r'read'
t_AGAIN = r'again'
t_DEFER = r'defer'
t_FORGET = r'forget'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


t_ignore = " \t"

lexer = lex.lex()

# # Parsing rules
#
precedence = (
    # ('nonassoc', 'EQUALS'),
     ('left', 'AND', 'OR', 'NEGATE'),
     ('left', 'PLUS', 'MINUS'),
     ('left', 'TIMES', 'DIVIDE'),
     ('left', 'APPEND'),
     ('right', 'UMINUS')
)
#
# # dictionary of names
# names = {}
#
#

lines_no = set()

def p_start(t):
    '''start : lines'''
    t[0] = t[1]

def p_lines(t):
    '''lines : line
              | line lines'''
    s = [s for s in t]
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = [t[1], *t[2]]

def p_line(t):
    '''line    :   NUMBER statements END
                |  NUMBER compounds statements END
    '''

    line_no = int(t[1])

    if line_no in lines_no:
        raise Exception("More than one line with the same number")

    lines_no.add(line_no)

    if len(t) == 4:
        defer = []
        again = []
        statements = t[2]
    else:
        defer, again = t[2]
        statements = t[3]

    t[0] = line_no, defer, again, [s for s in statements]


def p_compounds(t):
    '''compounds :    DEFER LPAREN booleanable RPAREN
                    | AGAIN LPAREN booleanable RPAREN
                    | DEFER LPAREN booleanable RPAREN compounds
                    | AGAIN LPAREN booleanable RPAREN compounds
    '''
    if len(t) == 5:
        additional_defer = []
        additional_again = []
    else:
        additional_defer, additional_again = t[5]

    if t.slice[1].type == "DEFER":
        defer = [t[3]]
        again = []
    else:
        defer = []
        again = [t[3]]

    t[0] = (defer + additional_defer, again + additional_again)

def p_booleanable(t):
    '''booleanable :  LPAREN booleanable RPAREN
                    | booleanable AND booleanable
                    | booleanable OR booleanable
                    | numerable
                    | numerable EQUALS numerable
                    | numerable GREATER_THAN numerable
                    | numerable GREATER_OR_EQUAL numerable
                    | numerable SMALLER_THAN numerable
                    | numerable SMALLER_OR_EQUAL numerable
                    | NEGATE booleanable
    '''
    if t.slice[1].type == "LPAREN":
        newt = t[2]
    elif len(t) == 2:
        # This might not actually be optimal for performance, but it's a way to simplify syntax
        newt = ("GREATER_THAN", ("COUNT", t[1]), ("PURE_NUMBER", 0))
    elif len(t) == 3:
        newt = (t.slice[1].type, t[2]) # NOT
    else:
        newt = (t.slice[2].type, t[1], t[3])
    t[0] = newt

def p_statements(t):
    '''statements   :  statement
                      | statement THEN statements
    '''
    if len(t) == 2:
        statements = [t[1]]
    else:
        statements = [t[1], *t[3]]
    t[0] = statements


def p_statement(t):
    '''statement :  PRINT LPAREN stringable RPAREN
                   | numerable
                   | numerable HASH numerable
   '''
    if t.slice[1].type == "PRINT":
        newt = (t.slice[1].type, t[3])
    else:
        newt = ("LINE_ADD_REMOVE", t[1], t[3] if len(t) == 4 else ('PURE_NUMBER' , 1))
    t[0] = newt

def p_stringable(t):
    '''stringable :  LPAREN stringable RPAREN
                   | pure_stringable
                   | number_stringable
                   | number_stringable PLUS stringable %prec APPEND
    '''
    if t.slice[1].type == "LPAREN":
        newt = t[2]
    elif len(t) == 2:
        if t[1][0][0] in ["NUMBER_2_STRING", "UNICODE_2_CHAR", "PURE_STRING"]:
            newt = t[1]
        else:
            newt = [("NUMBER_2_STRING", t[1])]
    else:
        if t[3][0][0] == "NUMBER_2_STRING":
            newt = [("NUMBER_2_STRING", operation_calc("PLUS", t[1], t[3][0][1]))] + t[3][1:]
        else:
            newt = [("NUMBER_2_STRING", t[1])] + t[3]
    t[0] = newt

def p_number_stringable(t): # This is different so that the string handle can take care of the '+' sign
    '''number_stringable : NUMBER
                    | READ
                    | number_stringable MINUS number_stringable
                    | number_stringable TIMES number_stringable
                    | number_stringable DIVIDE number_stringable
                    | COUNT LPAREN numerable RPAREN '''
    numerable_process(t)


def p_pure_stringable(t):
    '''pure_stringable : UNICODE LPAREN numerable RPAREN
                   | STRING
                   | STRING PLUS stringable  %prec APPEND
    '''
    if t.slice[1].type == "UNICODE":
        newt = [("UNICODE_2_CHAR", t[3])]
    else:
        string = t[1][1:-1]
        if len(t) == 2:
            newt = [("PURE_STRING", string)]
        else:
            if t[3][0][0] == "PURE_STRING":
                newt = [("PURE_STRING", string + t[3][0][1])] + t[3][1:]
            else:
                newt = [("PURE_STRING", string )] + t[3]
    t[0] = newt

def p_numerable(t):
    '''numerable :   NUMBER
                    | READ
                    | numerable PLUS numerable
                    | numerable MINUS numerable
                    | numerable TIMES numerable
                    | numerable DIVIDE numerable
                    | COUNT LPAREN numerable RPAREN 
                    | MINUS numerable %prec UMINUS
                    | LPAREN numerable RPAREN '''
    numerable_process(t)

def numerable_process(t):
    if t.slice[1].type == "LPAREN":
        newt = t[2]
    elif(len(t)==4):
        newt = operation_calc(t.slice[2].type, t[1], t[2])
    elif (len(t)==3):
            newt = ("TIMES", ("PURE_NUMBER", -1), t[2])
    elif (len(t) == 2):
        if t.slice[1].type == "READ":
            newt = (t.slice[1].type)
        else:
            newt = ("PURE_NUMBER", int(t[1]))
    else:
        newt = (t.slice[1].type, t[3]) # COUNT
    t[0] = newt

def operation_calc(symbol, array1, array2):
    if array1[0] == "PURE_NUMBER" and array2[0] == "PURE_NUMBER":
        # This may be unnecessary but simplifies the end result
        if symbol == "PLUS":
            newt = ("PURE_NUMBER", array1[1] + array2[1])
        elif symbol == "MINUS":
            newt = ("PURE_NUMBER", array1[1] - array2[1])
        elif symbol == "TIMES":
            newt = ("PURE_NUMBER", array1[1] * array2[1])
        elif symbol == "DIVIDE" and array2[1] != 0:
            newt = ("PURE_NUMBER", array1[1] / array2[1])
        else:
            raise Exception("INVALID MATH OPERATION")
    else:
        newt = (symbol, array1, array2)
    return newt

def p_error(t):
     print("Syntax error at '%s'" % t.value)

parser = yacc.yacc()

def code_to_tree(code, path, picklefy=True):
    global lines_no
    lines_no = set()
    tree = parser.parse(code)
    if picklefy:
        with open(f'{path}.pkl', 'wb') as f:
            pickle.dump(tree, f)
    return tree

def load_tree(path):
    with open(f'{path}.pkl', 'rb') as f:
        loaded_array = pickle.load(f)
    return loaded_array

if __name__ == "__main__":
    raise Exception("Nope")
    from example_whenever_codes.example_whenever_code import example_code, example_code2, example_code3
    code_to_tree(example_code, "test")
    code_to_tree(example_code2, "test2")
    code_to_tree(example_code3, "test3")