from __nonstandard__ import french_syntax

def test_bool():
    assert Vrai, "Vrai is True"
    assert not Faux, "Faux is False"

def test_for():
    total = 0
    pour i dans intervalle(10):
        total += i
    assert total == 45
