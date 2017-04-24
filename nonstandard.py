''' A custom Importer making use of the import hook capability

https://www.python.org/dev/peps/pep-0302/

When a module is imported, it simply adds a line to its source code 
prior to execution.

This code was adapted from
http://stackoverflow.com/questions/43571737/how-to-implement-an-import-hook-that-can-modify-the-source-code-on-the-fly-using/43573798#43573798
which is a question I asked.
'''
import re
import sys
import os.path

from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location

MAIN = False
from_nonstandard = re.compile("(^from\s+__nonstandard__\s+import\s+)")
included_transformers_path = os.path.join(os.path.dirname(__file__), 
                                          "transformers")
_imposed_transformers = []

def impose_transformer(name):
    _imposed_transformers.append(name)

class _MyMetaFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if not path:
            path = [os.getcwd(), included_transformers_path]
        if "." in fullname:
            name = fullname.split(".")[-1]
        else:
            name = fullname
        for entry in path:
            if os.path.isdir(os.path.join(entry, name)):
                # this module has child modules
                filename = os.path.join(entry, name, "__init__.py")
                submodule_locations = [os.path.join(entry, name)]
            else:
                filename = os.path.join(entry, name + ".py")
                submodule_locations = None
            if not os.path.exists(filename):
                continue

            return spec_from_file_location(fullname, 
                filename, 
                loader=_MyLoader(filename),
                submodule_search_locations=submodule_locations)
        return None # we don't know how to import this

sys.meta_path.insert(0, _MyMetaFinder())


class _MyLoader(Loader):
    def __init__(self, filename):
        self.filename = filename

    def create_module(self, spec):
        return None # use default module creation semantics

    def exec_module(self, module):
        global MAIN
        with open(self.filename) as f:
            source = f.read()

        if _imposed_transformers:  
            source = _transform(source)
        else:
            for linenumber, line in enumerate(source.split('\n')):
                if from_nonstandard.match(line):
                    source = _transform(source)
                    break

        exec(source, vars(module))
        if MAIN:
            module.__name__ = "__main__"
            MAIN = False

def _transform(source):
    '''Used to convert the source code, and create a new module
       if one of the lines is of the form

           ^from __nonstandard__ import transformer1 [, transformer2, ...]

       (where ^ indicates the beginning of a line)
       otherwise returns None and lets the normal import take place.
       Note that this special code must be all on one physical line --
       no continuation allowed by using parentheses or the
       special \ end of line character.

       "transformers" are modules which must contain a function

           transform_source_code(source)

       which returns a tranformed source.
    '''
    lines = source.split('\n')
    transformers = []
    linenumbers = []
    for number, line in enumerate(lines):
        if from_nonstandard.match(line):
            # we started with: "from __nonstandard__ import transformer1 [,...]"
            line = from_nonstandard.sub(' ', line)
            # we now have: " transformer1 [,...]"
            line = line.split("#")[0]    # remove any end of line comments
            # and insert each transformer as an item in a list
            transformers.extend(line.replace(' ', '').split(','))
            linenumbers.insert(0, number)

    # drop the "fake" import from the source code
    for number in linenumbers:
        del lines[number]
    source = '\n'.join(lines)

    transformers.extend(_imposed_transformers)
    for transformer in transformers:
        mod_name = __import__(transformer)
        source = mod_name.transform_source(source)
    return source


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # this program was started by
        # $ python import_experimental.py some_script
        # and we will want some_script.__name__ == "__main__"
        MAIN = True
        __import__(sys.argv[1])