
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import nonstandard

def single_file_test(script, prefix="test_"):
    for name in dir(script):
        if name.startswith(prefix):
            getattr(script, name)()
            print("Successfully tested function", name)
