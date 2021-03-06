
The content of this readme has been automatically extracted from
the docstring of each file found in this directory.

Note that multiple transforms can be used in a single file, e.g.

    from __nonstandard__ import increment, decrement
    from __nonstandard__ import function_keyword


## convert_py2.py 

    from __nonstandard__ import convert_py2

triggers the use of the lib2to3 Python library to automatically convert
the code from Python 2 to Python 3 prior to executing it.

As long as lib2to3 can convert the code, this means that code written
using Python 2 syntax can be run using a Python 3 interpreter.


## decrement.py 


    from __nonstandard__ import decrement

enables transformation of code of the form
    
    name --  # optional comment

into 

    name -= 1  # optional comment

Space(s) betwen `name` and `--` are ignored.

This can change not only code but content of triple quoted strings
as well. A more robust solution could always be implemented 
using the tokenize module.


## french_syntax.py 

    from __nonstandard__ import french_syntax

allows the use of a predefined subset of Python keyword to be written
as their French equivalent; English and French keywords can be mixed.

Thus, code like:

    si Vrai:
        imprime("French can be used.")
    autrement:
        print(Faux)

Will be translated to

    if True:
        print("French can be used.")
    else:
        print(False)

This type of transformation could be useful when teaching the
very basic concepts of programming to (young) beginners who use 
non-ascii based language and would find it difficult to type
ascii characters. 


## function_keyword.py 

    from __nonstandard__ import function_keyword

enables to use the word `function` instead of `lambda`, as in

    square = function x: x**2

    square(3)  # returns 9


## increment.py 


    from __nonstandard__ import increment

enables transformation of code of the form
    
    name ++  # optional comment

into 

    name += 1  # optional comment

Space(s) betwen `name` and `++` are ignored.

This can change not only code but content of triple quoted strings
as well. A more robust solution could always be implemented 
using the tokenize module.


## nobreak_keyword.py 

    from __nonstandard__ import nobreak_keyword

enables to use the fake keyword `nobreak` instead of `else`, as in

    for i in range(3):
        print(i)
    nobreak:
        print("The entire loop was run.")

Note that `nobreak` can be use everywhere `else` could be used,
even if it does not make sense.


## pep542.py 

    from __nonstandard__ import pep542

Trying to implement https://www.python.org/dev/peps/pep-0542/


## print_keyword.py 

    from __nonstandard__ import print_keyword

triggers the use of the lib2to3 Python library to automatically convert
all `print` statements (assumed to use the Python 2 syntax) into
function calls.


## repeat_keyword.py 

    from __nonstandard__ import repeat_keyword

introduces `repeat` as a keyword to write simple loops that repeat
a set number of times.  That is:

    repeat 3:
        a = 2
        repeat a*a:
            pass

is equivalent to

    for __VAR_1 in range(3):
        a = 2
        for __VAR_2 in range(a*a):
            pass

The names of the variables are chosen so as to ensure that they
do not appear in the source code to be translated.


## where_clause.py 

    from __nonstandard__ import where_clause

shows how one could use `where` as a keyword to introduce a code
block that would be ignored by Python. The idea was to use this as
a _pythonic_ notation as an alternative for the optional type hinting described
in PEP484.  **This idea has been rejected; it is included just for fun.**

Note that this transformation **cannot** be used in the console.

For more details, please see two of my recent blog posts:

https://aroberge.blogspot.ca/2015/12/revisiting-old-friend-yet-again.html

https://aroberge.blogspot.ca/2015/01/type-hinting-in-python-focus-on.html

I first suggested this idea more than 12 years ago! ;-)

https://aroberge.blogspot.ca/2005/01/where-keyword-and-python-as-pseudo.html
