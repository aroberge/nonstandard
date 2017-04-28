try:
    from .common import nonstandard
    from .where_testfile import *
except SystemError:
    import common
    import where_testfile
    common.single_file_test(where_testfile)
