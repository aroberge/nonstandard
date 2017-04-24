''' A custom Importer making use of the import hook capability

https://www.python.org/dev/peps/pep-0302/

When a module is imported, it simply adds a line to its source code 
prior to execution.

This code was adapted from
http://stackoverflow.com/questions/43571737/how-to-implement-an-import-hook-that-can-modify-the-source-code-on-the-fly-using/43573798#43573798
which is a question I asked.
'''
import code
import re
import sys
import os.path

from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location

from_nonstandard = re.compile("(^from\s+__nonstandard__\s+import\s+)")
included_transformers_path = os.path.join(os.path.dirname(__file__), 
                                          "transformers")

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
        global other_is_main  # defined at the bottom of this file
        if other_is_main:
            module.__name__ = "__main__"
            other_is_main = False

        with open(self.filename) as f:
            source = f.read()

        if transformers:  
            source = _transform(source)
        else:
            for linenumber, line in enumerate(source.split('\n')):
                if from_nonstandard.match(line):
                    source = _transform(source)
                    break

        exec(source, vars(module))


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


class NonStandardInteractiveConsole(code.InteractiveConsole):
    LINETRANSFORM = True
    def push(self, line):
        """Push a line to the interpreter.

        The line should not have a trailing newline; it may have
        internal newlines.  The line is appended to a buffer and the
        interpreter's runsource() method is called with the
        concatenated contents of the buffer as source.  If this
        indicates that the command was executed or invalid, the buffer
        is reset; otherwise, the command is incomplete, and the buffer
        is left as it was after the line was appended.  The return
        value is 1 if more input is required, 0 if the line was dealt
        with in some way (this is the same as runsource()).

        """
        if line.strip() == "enable_block_transform":
            self.LINETRANSFORM = False
            line = ""

        if from_nonstandard.match(line):
            add_transformers(line)
        else:
            if self.LINETRANSFORM:
                line = _transform(line)
            self.buffer.append(line)

        source = "\n".join(self.buffer)
        if not self.LINETRANSFORM:
            source = _transform(source)
        more = self.runsource(source, self.filename)
        if not more:
            self.resetbuffer()
        return more

banner = "Non-standard Python interpreter\nPython version: %s\n" % sys.version
def start_console():
    sys.ps1 = "~~> "
    console = NonStandardInteractiveConsole()
    try:
        console.interact(banner=banner)
    except SystemExit:
        print("Leaving non-standard interpreter.\n")
        sys.ps1 = ">>> "


# The only situation in which we do not start an interactive console
# is when we run a single script using
# python nonstandard.py script

other_is_main = False
if __name__ == '__main__':
    if len(sys.argv) > 1:
        # this program was started by
        # $ python nonstandard.py some_script
        # and we will want some_script.__name__ == "__main__"
        other_is_main = True
        __name__ = __file__.split(".")[0]
        __import__(sys.argv[1])
        if sys.flags.interactive:
            start_console()
    else:
        start_console()
else:
    start_console()


