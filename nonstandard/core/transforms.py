
import re
import sys

from_nonstandard = re.compile("(^from\s+__nonstandard__\s+import\s+)")


transformers = set([])
def add_transformers(line):
    assert from_nonstandard.match(line)

    # We are adding a transformer built from normal/standard Python code.
    # As we are not performing transformations, we temporarily disable
    # our import hook, both to avoid potential problems AND because we
    # found that this resulted in much faster code.
    hook = sys.meta_path[0]
    sys.meta_path = sys.meta_path[1:]

    # we started with: "from __nonstandard__ import transformer1 [,...]"
    line = from_nonstandard.sub(' ', line)
    # we now have: " transformer1 [,...]"
    line = line.split("#")[0]    # remove any end of line comments
    # and insert each transformer as an item in a list
    for trans in line.replace(' ', '').split(','):
        try:
            __import__(trans)
        except ImportError:
            print("Import Error: %s not found" % trans)
            continue
        transformers.add(trans)

    # resume import hook
    sys.meta_path.insert(0, hook)


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
        print("          transformer: ", transformer)
        mod_name = __import__(transformer)
        try:
            source = mod_name.transform_source(source)
            # may raise an AttributeError at first from the interactive console
            if not source.startswith("'''"):
                print("source = ", source.replace("\n", "|"))
        except AttributeError:
            pass
    return source
