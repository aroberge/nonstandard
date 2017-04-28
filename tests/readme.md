# About these tests

For simplicity, I use [pytest](https://docs.pytest.org/en/latest/contents.html)'s strategy of simply using Python's `assert` statements and naming test files and test functions within these files all starting with `test_` for easy discovery. `pytest` is not part of Python's standard library and you may have to intall it. (If you use the Python Anaconda distribution from Continuum Analytics, it is likely already included.)

 However, since `nonstandard` changes the way `import` works, the _normal_ approach used by `pytest` is modified.  For each test, two files are created:

    test_X.py
    X.py

`X.py` is the actual file that contains the tests for the nonstandard, and almost always invalid Python syntax.  As such, it cannot be imported by the normal mechanism.  `test_X.py` imports `nonstandard`, which install an import hook. It then imports `X.py` which can be processed by the `nonstandard` import hook.

`X.py`'s content should be something like:

    from __nonstandard__ import X_feature

    def test_one():
        ...
        assert something, "something is tested"
        ...

    def test_another():
        ...
        assert something_else, "something else is tested"
        ...

To ensure that the development version of `nonstandard` is used, `test_X.py` will first import a file (`common.py`) which changes `sys.path` to ensure that this is the case.

## Using only pytest

To write a series of tests that can be discovered by `pytest`, a file named `test_X` has only to contain two lines:

    from .common import nonstandard
    from .X import *

The second line will ensure that functions named `test_Y` are discovered by pytest. 

To run all tests from within the tests folder, the following can be used:

    python -m pytest .

## Running a single test without pytest 

To run a single test file `test_X.py` without using pytest, we need the file to contain the following three lines of code:

    import common
    import X
    common.single_file_test(X)

## Combining both approaches

For greater flexibility, the recommended content of file `test_X.py` should be the following:

    try:
        from .common import nonstandard
        from .X import *
    except ImportError:
        import common
        import X
        common.single_file_test(X)
