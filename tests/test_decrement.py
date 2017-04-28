try:
    from .common import nonstandard
    from .decrement_testfile import *
except SystemError:
    import common
    import decrement_testfile
    common.single_file_test(decrement_testfile)