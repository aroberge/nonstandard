try:
    from .common import nonstandard
    from .print_testfile import *
except SystemError:
    import common
    import print_testfile
    common.single_file_test(print_testfile)
