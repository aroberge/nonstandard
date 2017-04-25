'''A custom Importer making use of the import hook capability

Note that the protocole followed is no longer as described in PEP 302 [1]

This code was adapted from
http://stackoverflow.com/questions/43571737/how-to-implement-an-import-hook-that-can-modify-the-source-code-on-the-fly-using/43573798#43573798
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

main_module_name = None
def import_main(name):
    global main_module_name
    main_module_name = name 
    __import__(name)


class MyMetaFinder(MetaPathFinder):
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
                    source = transforms.transform(source)
                    break

        exec(source, vars(module))
