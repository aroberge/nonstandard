from __nonstandard__ import decrement, increment
from __nonstandard__ import french_syntax

def test_increment_decrement():
    a = 0
    a--
    a ++
    assert a == 0

def test_french():
    assert Vrai
