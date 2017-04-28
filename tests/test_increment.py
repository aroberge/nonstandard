try:
    from .common import nonstandard
    from .increment_testfile import *
except SystemError:
    import common
    import increment_testfile
    common.single_file_test(increment_testfile)
