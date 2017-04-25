
import re

from_nonstandard = re.compile("(^from\s+__nonstandard__\s+import\s+)")


transformers = set([])
def add_transformers(line):
    assert from_nonstandard.match(line)
    # we started with: "from __nonstandard__ import transformer1 [,...]"
    line = from_nonstandard.sub(' ', line)
    # we now have: " transformer1 [,...]"
    line = line.split("#")[0]    # remove any end of line comments
    # and insert each transformer as an item in a list
    for trans in line.replace(' ', '').split(','):
        transformers.add(trans)


def transform(source):
    '''Used to convert the source code, and create a new module
       if one of the lines is of the form

           ^from __nonstandard__ import transformer1 [, transformer2, ...]

       (where ^ indicates the beginning of a line)
       otherwise returns None and lets the normal import take place.
       Note that this special code must be all on one physical line --
       no continuation allowed by using parentheses or the
       special \ end of line character.

       "transformers" are modules which must contain a function

           transform_source(source)

       which returns a tranformed source.
    '''
    lines = source.split('\n')
    linenumbers = []
    for number, line in enumerate(lines):
        if from_nonstandard.match(line):
            add_transformers(line)
            linenumbers.insert(0, number)

    # drop the "fake" import from the source code
    for number in linenumbers:
        del lines[number]
    source = '\n'.join(lines)

    for transformer in transformers:
        mod_name = __import__(transformer)
        try:
            source = mod_name.transform_source(source)
            # may raise an exception at first from the interactive console
        except AttributeError:
            pass
    return source
