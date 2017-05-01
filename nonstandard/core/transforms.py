#pylint: disable W1401
import re
import sys

from_nonstandard = re.compile("(^from\s+__nonstandard__\s+import\s+)")

class NullTransformer:
    def transform_source(self, source):
        return source 

transformers = {}
def add_transformers(line):
    assert from_nonstandard.match(line)

    # we started with: "from __nonstandard__ import transformer1 [,...]"
    line = from_nonstandard.sub(' ', line)
    # we now have: " transformer1 [,...]"
    line = line.split("#")[0]    # remove any end of line comments
    # and insert each transformer as an item in a list
    for trans in line.replace(' ', '').split(','):
        import_transformer(trans)


def import_transformer(name):
    if name in transformers:
        return transformers[name]

    # We are adding a transformer built from normal/standard Python code.
    # As we are not performing transformations, we temporarily disable
    # our import hook, both to avoid potential problems AND because we
    # found that this resulted in much faster code.
    hook = sys.meta_path[0]
    sys.meta_path = sys.meta_path[1:]
    try:
        transformers[name] = __import__(name)
    except ImportError:
        print("Warning: Import Error in add_transformers: %s not found" % name)
        transformers[name] = NullTransformer()
    except Exception as e:
        print("Unexpected exception in transforms.import_transformer",
              e.__class__.__name__)
    finally:
        sys.meta_path.insert(0, hook) # restore import hook

    return transformers[name]

def extract_transformers_from_source(source):
    lines = source.split('\n')
    linenumbers = []
    for number, line in enumerate(lines):
        if from_nonstandard.match(line):
            add_transformers(line)
            linenumbers.insert(0, number)

    # drop the "fake" import from the source code
    for number in linenumbers:
        del lines[number]
    return '\n'.join(lines)


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
    source = extract_transformers_from_source(source)

    not_done = transformers
    while True:
        failed = {}
        for name in not_done:
            tr_module = import_transformer(name)
            try:
                source = tr_module.transform_source(source)
            except Exception as e:
                failed[name] = tr_module
                print("Unexpected exception in transforms.transform",
                      e.__class__.__name__)

        if not failed:
            break
        if failed == not_done:
            print("Warning: the following transforms could not be done:")
            for key in failed:
                print(key)
            break
        not_done = failed  # attempt another pass

    return source
