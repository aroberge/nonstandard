from __nonstandard__ import pep542

def test_pep542():
    class MyClass:
        pass

    def MyClass.square(self, x):
        return x**2

    a = MyClass()

    def a.out():
        return 42

    assert a.out() == 42
    assert a.square(3) == 9
