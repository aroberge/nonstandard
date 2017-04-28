try:
    from .common import nonstandard
    from .multiple_transforms import *
except SystemError:
    import common
    import multiple_transforms
    common.single_file_test(multiple_transforms)
