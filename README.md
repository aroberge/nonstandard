
### A bit of nostalgia
```python
> python -m nonstandard
nonstandard console. [Python version: 3.5.2]

~~> from __nonstandard__ import print_keyword
~~> print "Hello world!"
Hello world!
```

# What is `nonstandard`?

`nonstandard` is a simple Python module intended to facilitate exploring different syntax construct in Python in an easy way.  Unless you have a very compelling reason to do so, it should not be used in production. The

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

## Usage overview

There are many ways to use `nonstandard`. 

### Alternative Python console
If you simply want to have start a nonstandard Python console, as shown at the top of this readme file, type 

    python -m nonstandard

### Automatically processing a file - 1

Simply add the name of the test file (without the .py extension) at the end.

```python
> type test.py
from __nonstandard__ import print_keyword
print "Hello world!"

> python -m nonstandard test
Hello world!
```

### Automatically processing a file - 2

You can also activate some transformations by inserting them between `nonstandard`
and the name of your python script on the command line.

```python
> type test.py
print "Hello world!"

> python -m nonstandard print_keyword test
Hello world!
```

### Automatically processing a file and activating a console

Like normal Python, you can execute a script and start an interactive session
afterwards by using the `-i` flag

```python
> type test.py
print "Hello world!"
my_variable = 3

> python -i -m nonstandard print_keyword test
Hello world!
nonstandard console. [Python version: 3.5.2]

~~> my_variable
3
```

_Note that there are two more **readme** files, one in the tests directory and the other in the nonstandard.transformers directory._


## To do

[ ] Complete readme

[ ] Add code/warning to remove code-block based transformations for console 

[ ] Add code transformation illustrating rejected PEP 315  (do while)

[ ] Add code transformation illustrating rejected PEP 284 (for lower <= var < upper:)

[x] Add code transformation illustrating new PEP 542 (dot assignment in functions)

[ ] Add version based on imp for older Python versions.
