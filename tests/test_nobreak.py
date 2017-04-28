try:
    from .common import nonstandard
    from .nobreak_testfile import *
except SystemError:
    import common
    import nobreak_testfile
    common.single_file_test(nobreak_testfile)
