try:
    from .common import nonstandard
    from .repeat_testfile import *
except SystemError:
    import common
    import repeat_testfile
    common.single_file_test(repeat_testfile)
