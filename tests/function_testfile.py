from __nonstandard__ import function_keyword

def test_function():
    square = function x: x**2
    assert square(3) == 9
