try:
    from .common import nonstandard
    from .french_testfile import *
except SystemError:
    import common
    import french_testfile
    common.single_file_test(french_testfile)
