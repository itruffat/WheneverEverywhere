# Whenever Transpiler 

### Introduction

The transpiler is the part that turns the AST (previously obtained in the `Whenever_parser`) into a completely 
stand-alone C file. To do this, we make use of `template.c`, which is an autonomous Whenever-engine coded in C. The code
simply changes some macro variables to make certain decisions about the final code (such as how to log information for 
debugging purposes) and adds the lines as functions. 


Example:


    Line in Whenever:
    ~~~~~~~~~~~~~~~~
      8 defer (N(7)<100) -1#N(1),-2#N(2),-7#100,-3;
    
    Line Compiled as a C Function:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      void F7_for_line8(void) { 
          // Indexes start at 0 in C, so everything is moved one space to the left
          bool defer = False  || ( (executionStack[6].count) < (100));
          if(!defer){
              bool again = False;
              // Starting statements 
              change_pos_quantity(0,_times(-1,executionStack[0].count));
              change_pos_quantity(1,_times(-1,executionStack[1].count));
              change_pos_quantity(6,-100);
              change_pos_quantity(2,-1);
              // Statements done
              if(!again) change_pos_quantity(7, -1);
          }
      }

As such, the code is **NOT** an interpreter with an attached input that's fetched at runtime, but a program that 
only does what the original code did. This might look like a small difference, but it's relevant to understand the
relative simplicity of the code. (as it does not need to go through the AST)

### Template.c

The file `template.c` is hardly perfect, relaying a lot on macros to remove the customization responsibility from the
python code. Being a in a single file also makes it harder to read than it should, given that what the codes is actually 
incredibly simple. While both of this critics are valid, they are the price to pay to make the code stand-alone and 
customizable.

The file works by keeping a list of each line and how many times they appear. 