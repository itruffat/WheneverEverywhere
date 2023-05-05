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

## Dev

Versioning should be written in 'version.info' and match the tags. For that one can use 
the hook script present in this repo:

    git config --local core.hooksPath .custom_git_hooks/

## TODO

* Make a more direct way of compiling, don't relay on the user knowing how to transpile  
 from C.
* Read in C works slightly different than in python. (it assumes that the final '\n' is a 
character and not the end of the line)
* 64-bits mode in C is not working either, the limit of an C int for values may be too low.
* Improve all the quick-n-dirty snippets, including IO handling, templating, logging, etc.