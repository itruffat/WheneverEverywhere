# Whenever Everywhere
#### A python-interpreter and compiler for the Whenever language

["Whenever" is an esoteric programming language](https://www.dangermouse.net/esoteric/whenever.html) 
in which the lines do not have a fixed order, and will eventually run. As such, the interesting 
thing is manipulating safeguards so lines are executed in an order that "does something".

**Whenever Everywhere** transforms Whenever code into an AST, allowing not only the creation of 
a new interpreter in Python, but also to transpiled into machine code by first compiling it 
into a C file. This is where "EVERYWHERE" comes in, as now the pieces of code can be used on
any machine/virtual machine that runs c, including the web via web assembly.

## How to use

Simply run the python script, with either "run" (for the interpreter) or "c" (for the compiler).

     python3 main.py run <filepath>

or

     python3 main.py c <filepath>

## TODO

* "Read" is still not implemented in C, need to get that going.
* Make a more direct way of transpiling, don't relay on the user knowing how to compile C.
* 64-bits mode in C is not working either, the limit of an C int for values may be too low.
* Improve all the quick-n-dirty snippets, including IO handling, templating, logging, etc.