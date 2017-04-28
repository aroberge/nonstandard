
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import nonstandard

def single_file_test(script):
    for name in dir(script):
        if name.startswith("test_"):
            getattr(script, name)()
            print("tested ", name)
