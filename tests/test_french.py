try:
    from .common import nonstandard
    from .french import *
except ImportError:
    import common
    import french
    common.single_file_test(french)
