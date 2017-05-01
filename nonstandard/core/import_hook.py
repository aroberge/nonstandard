'''A custom Importer making use of the import hook capability

Note that the protocole followed is no longer as described in PEP 302 [1]

This code was adapted from
http://stackoverflow.com/q/43571737/558799
which is a question I asked when I wanted to adopt an approach using
a deprecated module (imp) and which followed PEP 302.

[1] https://www.python.org/dev/peps/pep-0302/
'''

import os.path
import sys

from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location

from . import transforms

included_transformers_path = os.path.abspath(
                                os.path.join(os.path.dirname(__file__),
                                             "..", 
                                             "transformers" )) 
sys.path.append(included_transformers_path)

main_module_name = None
def import_main(name):
    global main_module_name
    main_module_name = name 
    return __import__(name)


class MyMetaFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if not path:
            path = [os.getcwd()]#, included_transformers_path]
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
                loader=MyLoader(filename),
                submodule_search_locations=submodule_locations)
        return None # we don't know how to import this

sys.meta_path.insert(0, MyMetaFinder())

class MyLoader(Loader):
    def __init__(self, filename):
        self.filename = filename

    def create_module(self, spec):
        return None # use default module creation semantics

    def exec_module(self, module):
        global main_module_name
        if module.__name__ == main_module_name:
            module.__name__ = "__main__"
            main_module_name = None

        with open(self.filename) as f:
            source = f.read()

        if transforms.transformers: 
            source = transforms.transform(source)
        else:
            for linenumber, line in enumerate(source.split('\n')):
                if transforms.from_nonstandard.match(line):
                    ## transforms.transform will extract all such relevant
                    ## lines and add them all relevant transformers
                    source = transforms.transform(source)
                    break
        exec(source, vars(module))

    def get_code(self, fullname):
        # hack to silence an error when running nonstandard as main script
        # See below for an explanation
        return compile("None", "<string>", 'eval')

"""
When this code was run as part of a normal script, no error was raised.
When I changed it into a package, and tried to run it as a module, an 
error occurred as shown below. By looking at the sources for the
importlib module, I saw that some classes had a get_code() method which
returned a code object.  Rather than trying to recreate all the code,
I wrote the above hack which seems to silence any error.

$ python -m nonstandard
Python version: 3.5.2 |Anaconda 4.2.0 (64-bit)| ...

    Python console with easily modifiable syntax.

~~> exit()
Leaving non-standard console.

Traceback (most recent call last):
  ...
  AttributeError: 'MyLoader' object has no attribute 'get_code'

"""
