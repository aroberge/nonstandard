# nonstandard

If you want to modify Python's syntax, say by adding a new keyword, you need to:

1. Get a copy of Python's repository on your computer
2. modify the grammar file 
3. modify the lexer
4. modify the parser
5. modify the compiler
6. recompile all the sources

This is a very involved process.  There has to be a better way if one just want to try some quick experiment.

`nonstandard` is a Python module that provides a much simpler way to experiment with changes to Python's syntax.

## Installation

To install `nonstandard`, you can use the standard way:

    pip install nonstandard

## Usage

There are many ways to use `nonstandard`. If you simply want to have start a Python console, type 

    python -m nonstandard

More to come ...


## To do

[ ] Complete readme
[ ] Add code/warning to remove code-block based transformations for console 
[ ] Add code transformation illustrating rejected PEP 315  (do while)
[ ] Add code transformation illustrating rejected PEP 284 (for lower <= var < upper:)
[ ] Add code transformation illustrating new PEP 542 (dot assignment in functions)
[ ] Add version based on imp for older Python versions.
