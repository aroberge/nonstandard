try:
    from .common import nonstandard
    from .function_testfile import *
except SystemError:
    import common
    import function_testfile
    common.single_file_test(function_testfile)
