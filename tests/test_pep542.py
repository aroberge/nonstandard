try:
    from .common import nonstandard
    from .pep542_testfile import *
except SystemError:
    import common
    import pep542_testfile
    import nobreak_testfile
    common.single_file_test(pep542_testfile)
